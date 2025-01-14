; Interface assembly file
bits 64
default rel

; External functions from C runtime
extern printf
extern malloc
extern free
extern memcpy

; Include debug macros
%include "debug.inc"

; Data section
section .data
    str_alloc_error db "Failed to allocate memory", 0
    str_alloc_success db "Successfully allocated %d bytes at %p", 0
    str_free_memory db "Freeing memory at %p", 0
    str_copy_memory db "Copying %d bytes from %p to %p", 0
    str_init_function db "initialize_interface", 0
    str_alloc_function db "allocate_memory", 0
    str_free_function db "free_memory", 0
    str_copy_function db "copy_memory", 0

; Code section
section .text
global initialize_interface
global allocate_memory
global free_memory
global copy_memory

; Function: initialize_interface
; Description: Initializes the interface
initialize_interface:
    FUNCTION_ENTRY str_init_function
    
    ; Your initialization code here
    xor rax, rax    ; Return 0 for success
    
    FUNCTION_EXIT str_init_function
    ret

; Function: allocate_memory
; Parameters:
;   rcx - Size in bytes to allocate
; Returns:
;   rax - Pointer to allocated memory or NULL on failure
allocate_memory:
    FUNCTION_ENTRY str_alloc_function
    
    ; Save parameters
    push rbp
    mov rbp, rsp
    push rcx        ; Save size parameter
    
    ; Call malloc
    sub rsp, 32     ; Shadow space for Windows x64 calling convention
    call malloc
    add rsp, 32
    
    ; Check if allocation succeeded
    test rax, rax
    jz .allocation_failed
    
    ; Log success
    push rax
    sub rsp, 32
    lea rcx, [str_alloc_success]
    mov rdx, [rbp-8]    ; Original size
    mov r8, rax         ; Allocated pointer
    call printf
    add rsp, 32
    pop rax
    
    jmp .exit
    
.allocation_failed:
    ; Log error
    ERROR_LOG str_alloc_error
    xor rax, rax        ; Return NULL
    
.exit:
    pop rcx
    pop rbp
    FUNCTION_EXIT str_alloc_function
    ret

; Function: free_memory
; Parameters:
;   rcx - Pointer to memory to free
free_memory:
    FUNCTION_ENTRY str_free_function
    
    ; Log the free operation
    push rcx            ; Save pointer
    sub rsp, 32
    lea rcx, [str_free_memory]
    mov rdx, [rsp+40]  ; Get original pointer
    call printf
    add rsp, 32
    pop rcx
    
    ; Call free
    sub rsp, 32
    call free
    add rsp, 32
    
    FUNCTION_EXIT str_free_function
    ret

; Function: copy_memory
; Parameters:
;   rcx - Destination pointer
;   rdx - Source pointer
;   r8  - Size in bytes to copy
; Returns:
;   rax - Destination pointer
copy_memory:
    FUNCTION_ENTRY str_copy_function
    
    ; Save parameters
    push rbp
    mov rbp, rsp
    push rcx    ; Save destination
    push rdx    ; Save source
    push r8     ; Save size
    
    ; Log the copy operation
    sub rsp, 32
    lea rcx, [str_copy_memory]
    mov rdx, r8          ; Size
    mov r8, [rbp-16]    ; Source
    mov r9, [rbp-8]     ; Destination
    call printf
    add rsp, 32
    
    ; Call memcpy
    mov rcx, [rbp-8]    ; Destination
    mov rdx, [rbp-16]   ; Source
    mov r8, [rbp-24]    ; Size
    sub rsp, 32
    call memcpy
    add rsp, 32
    
    ; Return destination pointer
    mov rax, [rbp-8]
    
    ; Cleanup and exit
    pop r8
    pop rdx
    pop rcx
    pop rbp
    
    FUNCTION_EXIT str_copy_function
    ret
