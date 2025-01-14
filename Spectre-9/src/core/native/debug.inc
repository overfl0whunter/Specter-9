; Debug macros for assembly
%ifndef DEBUG_INC
%define DEBUG_INC

%ifdef _DEBUG
    %define DEBUG_ENABLED 1
%else
    %define DEBUG_ENABLED 0
%endif

; String constants
section .data
    str_function_entry db "Entering function: %s", 0
    str_function_exit db "Exiting function: %s", 0
    str_debug db "[DEBUG] %s", 0
    str_error db "[ERROR] %s", 0
    str_warning db "[WARNING] %s", 0
    str_memory_dump db "Memory dump at %p: ", 0
    str_hex_format db "%02X ", 0
    str_newline db 0xD, 0xA, 0

; Debug logging macro
%macro DEBUG_LOG 1
    %if DEBUG_ENABLED
        push rdi
        push rsi
        push rcx
        sub rsp, 32                  ; Reserve shadow space
        lea rcx, [str_debug]         ; Format string
        lea rdx, [%1]               ; Message
        call printf
        lea rcx, [str_newline]
        call printf
        add rsp, 32                  ; Restore stack
        pop rcx
        pop rsi
        pop rdi
    %endif
%endmacro

; Error logging macro
%macro ERROR_LOG 1
    push rdi
    push rsi
    push rcx
    sub rsp, 32                      ; Reserve shadow space
    lea rcx, [str_error]             ; Format string
    lea rdx, [%1]                   ; Message
    call printf
    lea rcx, [str_newline]
    call printf
    add rsp, 32                      ; Restore stack
    pop rcx
    pop rsi
    pop rdi
%endmacro

; Function entry logging macro
%macro FUNCTION_ENTRY 1
    %if DEBUG_ENABLED
        push rdi
        push rsi
        push rcx
        sub rsp, 32                  ; Reserve shadow space
        lea rcx, [str_function_entry] ; Format string
        lea rdx, [%1]               ; Function name
        call printf
        lea rcx, [str_newline]
        call printf
        add rsp, 32                  ; Restore stack
        pop rcx
        pop rsi
        pop rdi
    %endif
%endmacro

; Function exit logging macro
%macro FUNCTION_EXIT 1
    %if DEBUG_ENABLED
        push rdi
        push rsi
        push rcx
        sub rsp, 32                  ; Reserve shadow space
        lea rcx, [str_function_exit]  ; Format string
        lea rdx, [%1]               ; Function name
        call printf
        lea rcx, [str_newline]
        call printf
        add rsp, 32                  ; Restore stack
        pop rcx
        pop rsi
        pop rdi
    %endif
%endmacro

; Memory dump macro (dumps n bytes starting at address)
%macro MEMORY_DUMP 2
    %if DEBUG_ENABLED
        push rdi
        push rsi
        push rcx
        push r8
        push r9
        push r10
        sub rsp, 32                  ; Reserve shadow space
        
        ; Print header
        lea rcx, [str_memory_dump]
        mov rdx, %1                  ; Address
        call printf
        
        ; Loop through bytes
        mov r10, %2                  ; Number of bytes to dump
        mov r9, %1                   ; Current address
    %%dump_loop:
        test r10, r10
        jz %%dump_done
        
        ; Print byte in hex
        lea rcx, [str_hex_format]
        movzx rdx, byte [r9]
        call printf
        
        inc r9
        dec r10
        jmp %%dump_loop
        
    %%dump_done:
        lea rcx, [str_newline]
        call printf
        
        add rsp, 32                  ; Restore stack
        pop r10
        pop r9
        pop r8
        pop rcx
        pop rsi
        pop rdi
    %endif
%endmacro

%endif ; DEBUG_INC
