#include <windows.h>

// Funzioni esportate dall'assembly
extern void ExploitVBVA(void);
extern void ExploitSCSI(void);
extern void ExploitVRAM(void);

// DLL entry point
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            // Inizializzazione DLL
            break;
        case DLL_PROCESS_DETACH:
            // Cleanup DLL
            break;
    }
    return TRUE;
}

// Funzioni esportate
__declspec(dllexport) void RunVBVAExploit(void) {
    ExploitVBVA();
}

__declspec(dllexport) void RunSCSIExploit(void) {
    ExploitSCSI();
}

__declspec(dllexport) void RunVRAMExploit(void) {
    ExploitVRAM();
}
