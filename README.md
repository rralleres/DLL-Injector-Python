# 💉 Windows DLL Injector (Python) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/windows/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](#) 
A robust, educational tool for performing DLL injection on Windows systems. This project leverages the `ctypes` library to interface directly with the Windows API (`kernel32.dll`), demonstrating low-level memory allocation, process synchronization, and cross-language interoperability.# 💉 Windows DLL Injector (Python)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/windows/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](#)

A robust, educational tool for performing DLL injection on Windows systems. This project leverages the `ctypes` library to interface directly with the Windows API (`kernel32.dll`), demonstrating low-level memory allocation, process synchronization, and cross-language interoperability.

## 🚀 Key Features

-   **Flexible Targeting:** Inject by Process Name (`-n`) or PID (`-p`) using `psutil`.
    
-   **Architecture Validation:** Built-in "Bitness" check prevents crashes by ensuring Python, the DLL, and the Target Process all match (x64 vs x86).
    
-   **Execution Sync:** Uses `WaitForSingleObject` and `GetExitCodeThread` to verify if `LoadLibraryA` succeeded inside the target.
    
-   **Resource Management:** Strict handle cleanup using `try...finally` blocks to ensure system stability.
    

## 🛠️ Requirements

### 1. Runtime Environment (Windows) 
To run the `injector.py` script, you need: 
* **OS:** Windows 10 or 11.
* **Python:** 3.8+ (64-bit recommended for targeting 64-bit apps).
* **Permissions:** Administrator privileges (required to write to other processes).
* **Libraries:** Install via `pip install -r requirements.txt` (includes `psutil`).
### 2. Compilation Environment (To build the Sample DLL) 
You only need **one** of the following depending on your OS:
* **On Windows:** * [MinGW-w64](https://www.mingw-w64.org/) (for `gcc`) **OR** * [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/) (for `cl.exe`). 
* **On Linux (Cross-Compilation):** * `mingw-w64` package. 
```bash sudo apt install mingw-w64 ```
    

## 📂 Usage

### 1. Compile the Test DLL

Navigate to `src/sample_dll/` and run the batch script. It will automatically detect `gcc` (MinGW) or `cl` (Visual Studio) and build `hello_world.dll`.

**On Windows:** 

```
cd src/sample_dll
build_dll.bat

```

**On Linux (cross-compilation):** 
Ensure `mingw-w64` is installed, then run:
```
cd src/sample_dll
chmod +x build_dll.sh
./build_dll.sh

```
### 2. Run the Injector

Open a target process (e.g., `notepad.exe`) and execute the script. **Note: You must use the absolute path to your DLL.**


```
# Option A: Inject via Process Name
python src/injector.py -n notepad.exe -d C:\Users\Test\Project\src\sample_dll\hello_world.dll

# Option B: Inject via PID
python src/injector.py -p 1234 -d C:\Users\Test\Project\src\sample_dll\hello_world.dll

```

## ⚠️ Important Considerations

### 🛡️ Security & AV

Most modern Antivirus (AV) and Endpoint Detection and Response (EDR) solutions monitor the `CreateRemoteThread` API call. This tool is intended for **educational research and authorized testing only**. Using this on systems you do not own is illegal.

### 🏗️ Architecture (Bitness)

A 64-bit process **cannot** load a 32-bit DLL, and vice-versa.

-   If you use a 64-bit Python interpreter, you should target 64-bit processes and use a 64-bit DLL.
    
-   The script includes a pre-injection check to prevent memory corruption caused by architecture mismatches.
    

### 📍 Absolute Paths

The Windows `LoadLibrary` function searches for DLLs in specific directories. To ensure your injected DLL is found, always provide the **full absolute path** to the `-d` argument.

## 🔮 Future Improvements (Roadmap)

To evolve this from a basic Proof of Concept to an advanced security tool, I plan to implement:

-   **Manual Mapping:** Writing the PE headers manually to memory to bypass `LoadLibrary` hooks.
    
-   **APC Injection:** Utilizing `QueueUserAPC` for a stealthier injection footprint.
    
-   **Reflective Loading:** Enabling the DLL to map itself into memory without disk artifacts.
    
-   **Process Enumeration GUI:** A simple interface to pick processes from a list.
    
## 🔍 Troubleshooting

| Error / Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| **Error 5: Access Denied** | Lack of permissions to the target process. | Run your terminal/IDE as **Administrator**. |
| **Error 87: Invalid Parameter** | Often caused by a 32/64-bit mismatch. | Ensure Python, the DLL, and the Target are all the same architecture. |
| **DLL Loads but no Popup** | Windows cannot find the DLL file. | Use a **full absolute path** (e.g., `C:\Users\...`) instead of a relative one. |
| **ModuleNotFoundError** | Missing Python dependencies. | Run `pip install -r requirements.txt` to install `psutil`. |
| **Target Process Crashes** | Memory corruption or bitness conflict. | Double-check that you aren't injecting into a critical system process (like `lsass.exe`). |

### Common WinAPI Error Codes
If the script reports a `WinError`, these are the most frequent codes you'll encounter:

* **0x5 (ERROR_ACCESS_DENIED):** You don't have permission to `OpenProcess`. This happens if the target is a System process or owned by another user.
* **0x6 (ERROR_INVALID_HANDLE):** The Process ID (PID) provided may have closed before the script could finish its task.
* **0x7E (ERROR_MOD_NOT_FOUND):** `LoadLibraryA` failed inside the target because the path to your DLL was incorrect or inaccessible.
## 📝 License

This project is licensed under the MIT License
