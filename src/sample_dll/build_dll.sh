#!/bin/bash

# Configuration
DLL_NAME="hello_world.dll"
SOURCE_NAME="hello_world.c"

echo "[*] checking for mingw-w64 compiler..."

# Check for 64-bit compiler
if command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    echo "[+] Found 64-bit compiler. Building x64 DLL..."
    x86_64-w64-mingw32-gcc -shared -o $DLL_NAME $SOURCE_NAME -luser32
    echo "[+] Done: $DLL_NAME (64-bit)"
    exit 0
fi

# Check for 32-bit compiler if 64-bit isn't found
if command -v i686-w64-mingw32-gcc >/dev/null 2>&1; then
    echo "[+] Found 32-bit compiler. Building x86 DLL..."
    i686-w64-mingw32-gcc -shared -o $DLL_NAME $SOURCE_NAME -luser32
    echo "[+] Done: $DLL_NAME (32-bit)"
    exit 0
fi

echo "[-] Error: mingw-w64 not found. Install it with 'sudo apt install mingw-w64'"
exit 1
