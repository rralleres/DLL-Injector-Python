@echo off
SET DLL_NAME=hello_world.dll
SET SOURCE_NAME=hello_world.c

echo [*] Checking for compilers...

:: Check for GCC (MinGW)
where gcc >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [+] GCC found. Compiling...
    gcc -shared -o %DLL_NAME% %SOURCE_NAME% -luser32
    goto success
)

:: Check for MSVC (Visual Studio)
where cl >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [+] MSVC found. Compiling...
    cl.exe /LD %SOURCE_NAME% /Fe:%DLL_NAME% user32.lib
    goto success
)

echo [-] Error: No compatible compiler (GCC or MSVC) found in PATH.
pause
exit /b 1

:success
echo [+] Compilation successful: %DLL_NAME%
pause
