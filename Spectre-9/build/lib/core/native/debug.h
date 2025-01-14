#ifndef SPECTRE9_DEBUG_H
#define SPECTRE9_DEBUG_H

#include <windows.h>
#include <stdio.h>
#include <stdarg.h>

// Livelli di debug
#define DBG_NONE    0
#define DBG_ERROR   1
#define DBG_WARN    2
#define DBG_INFO    3
#define DBG_DEBUG   4
#define DBG_TRACE   5

// Colori per l'output
#define CLR_RED     FOREGROUND_RED | FOREGROUND_INTENSITY
#define CLR_YELLOW  FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY
#define CLR_WHITE   FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
#define CLR_CYAN    FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
#define CLR_GRAY    FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

// Macro per il debug
#ifdef _DEBUG
    #define DEBUG_LEVEL DBG_TRACE
#else
    #define DEBUG_LEVEL DBG_NONE
#endif

// Funzioni di debug
static HANDLE hDebugConsole = NULL;

static void InitDebug() {
    if (!hDebugConsole) {
        AllocConsole();
        hDebugConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    }
}

static void DebugPrint(int level, WORD color, const char* format, ...) {
    if (level > DEBUG_LEVEL) return;
    
    InitDebug();
    
    // Buffer per il timestamp
    char timestamp[32];
    SYSTEMTIME st;
    GetLocalTime(&st);
    sprintf_s(timestamp, sizeof(timestamp), 
        "[%02d:%02d:%02d.%03d] ",
        st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);
    
    // Imposta il colore
    SetConsoleTextAttribute(hDebugConsole, color);
    
    // Stampa timestamp
    WriteConsoleA(hDebugConsole, timestamp, strlen(timestamp), NULL, NULL);
    
    // Formatta e stampa il messaggio
    char buffer[4096];
    va_list args;
    va_start(args, format);
    vsprintf_s(buffer, sizeof(buffer), format, args);
    va_end(args);
    
    WriteConsoleA(hDebugConsole, buffer, strlen(buffer), NULL, NULL);
    WriteConsoleA(hDebugConsole, "\n", 1, NULL, NULL);
    
    // Ripristina il colore
    SetConsoleTextAttribute(hDebugConsole, CLR_WHITE);
}

// Macro per i diversi livelli di log
#define ERROR_LOG(fmt, ...) DebugPrint(DBG_ERROR, CLR_RED, "[ERROR] " fmt, ##__VA_ARGS__)
#define WARN_LOG(fmt, ...)  DebugPrint(DBG_WARN, CLR_YELLOW, "[WARN] " fmt, ##__VA_ARGS__)
#define INFO_LOG(fmt, ...)  DebugPrint(DBG_INFO, CLR_WHITE, "[INFO] " fmt, ##__VA_ARGS__)
#define DEBUG_LOG(fmt, ...) DebugPrint(DBG_DEBUG, CLR_CYAN, "[DEBUG] " fmt, ##__VA_ARGS__)
#define TRACE_LOG(fmt, ...) DebugPrint(DBG_TRACE, CLR_GRAY, "[TRACE] " fmt, ##__VA_ARGS__)

// Macro per il debug della memoria
#define DUMP_MEM(addr, size) DumpMemory(addr, size)

static void DumpMemory(void* addr, size_t size) {
    if (DEBUG_LEVEL < DBG_DEBUG) return;
    
    unsigned char* p = (unsigned char*)addr;
    char line[80];
    int offset = 0;
    
    while (offset < size) {
        int len = sprintf_s(line, sizeof(line), "%04X: ", offset);
        
        // Stampa hex
        for (int i = 0; i < 16 && offset + i < size; i++) {
            len += sprintf_s(line + len, sizeof(line) - len, 
                "%02X ", p[offset + i]);
        }
        
        // Padding
        while (len < 54) line[len++] = ' ';
        
        // Stampa ASCII
        for (int i = 0; i < 16 && offset + i < size; i++) {
            unsigned char c = p[offset + i];
            line[len++] = (c >= 32 && c <= 126) ? c : '.';
        }
        
        line[len++] = '\n';
        line[len] = 0;
        
        DEBUG_LOG("%s", line);
        offset += 16;
    }
}

// Macro per il debug delle funzioni
#define FUNCTION_ENTRY() TRACE_LOG("Entering %s", __FUNCTION__)
#define FUNCTION_EXIT()  TRACE_LOG("Exiting %s", __FUNCTION__)

// Macro per il debug delle syscall
#define SYSCALL_ENTRY(name) TRACE_LOG("Syscall %s - Entry", name)
#define SYSCALL_EXIT(name, status) TRACE_LOG("Syscall %s - Exit (status: %d)", name, status)

#endif // SPECTRE9_DEBUG_H
