#include <windows.h>

// The entry point for the DLL
BOOL APIENTRY DllMain(HMODULE hModule,  // Handle to DLL module
                       DWORD  ul_reason_for_call, // Reason for calling function
                       LPVOID lpReserved) // Reserved
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // This code runs as soon as the DLL is injected
        MessageBoxA(NULL, "Hello from the injected DLL!", "Injection Success", MB_OK | MB_ICONINFORMATION);
        break;

    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
