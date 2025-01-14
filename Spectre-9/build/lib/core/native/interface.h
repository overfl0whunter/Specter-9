#ifndef SPECTRE9_INTERFACE_H
#define SPECTRE9_INTERFACE_H

#include <windows.h>
#include <stdint.h>

// Strutture dati condivise
typedef struct {
    uint64_t vram_base;
    uint32_t vram_size;
    uint32_t flags;
} VRAM_CONFIG;

typedef struct {
    uint64_t buffer_addr;
    uint32_t buffer_size;
    uint32_t command_type;
} EXPLOIT_BUFFER;

// Codici di errore
#define SUCCESS                 0
#define ERR_INVALID_PARAMS    -1
#define ERR_MEMORY_MAP       -2
#define ERR_EXPLOIT_FAILED   -3

// Tipi di exploit
#define EXPLOIT_TYPE_SCSI     1
#define EXPLOIT_TYPE_VRAM     2
#define EXPLOIT_TYPE_VBVA     3

// Funzioni di interfaccia esportate
#ifdef __cplusplus
extern "C" {
#endif

// Funzioni di inizializzazione
__declspec(dllexport) int InitializeExploit(int exploit_type, void* config);
__declspec(dllexport) int CleanupExploit(int exploit_type);

// Funzioni per la manipolazione della memoria
__declspec(dllexport) int MapMemoryBuffer(uint64_t base_addr, uint32_t size);
__declspec(dllexport) int UnmapMemoryBuffer(uint64_t base_addr);

// Funzioni per l'esecuzione degli exploit
__declspec(dllexport) int PrepareExploitBuffer(EXPLOIT_BUFFER* buffer);
__declspec(dllexport) int TriggerExploit(int exploit_type);
__declspec(dllexport) int GetExploitStatus(int exploit_type);

// Funzioni di utilità
__declspec(dllexport) uint64_t GetModuleBase(const char* module_name);
__declspec(dllexport) int WriteMemory(uint64_t addr, const void* buffer, uint32_t size);
__declspec(dllexport) int ReadMemory(uint64_t addr, void* buffer, uint32_t size);

#ifdef __cplusplus
}
#endif

#endif // SPECTRE9_INTERFACE_H
