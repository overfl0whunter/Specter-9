@echo off
setlocal enabledelayedexpansion

echo [INFO] Configurazione ambiente build...

:: Configura NASM
echo [INFO] Configurazione NASM...
set "NASM_PATH=C:\NASM"
set "NASM_EXE=%NASM_PATH%\nasm.exe"

if not exist "%NASM_EXE%" (
    echo [ERRORE] NASM non trovato in %NASM_PATH%
    exit /b 1
)

:: Aggiungi NASM al PATH
set "PATH=%NASM_PATH%;%PATH%"
echo [SUCCESS] NASM configurato in %NASM_PATH%

:: Configurazione Visual Studio
echo [INFO] Configurazione ambiente Visual Studio...

:: Trova Visual Studio usando vswhere
for /f "usebackq tokens=*" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
    set "VSTOOLS=%%i"
)

if "%VSTOOLS%"=="" (
    echo [ERRORE] Visual Studio non trovato
    exit /b 1
)

echo [INFO] Trovato Visual Studio in: %VSTOOLS%

:: Configura l'ambiente di sviluppo Windows
echo [INFO] Configurazione Windows SDK...
set "WIN_SDK_ROOT=%ProgramFiles(x86)%\Windows Kits\10"
set "WIN_SDK_VERSION=10.0.22621.0"

:: Verifica che windows.h sia accessibile
echo [INFO] Verifica accesso a windows.h...
if exist "%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\um\windows.h" (
    echo [SUCCESS] windows.h trovato
) else (
    echo [ERRORE] windows.h non trovato in "%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\um\windows.h"
    exit /b 1
)

:: Configura Visual Studio Build Tools
echo [INFO] Configurazione ambiente x64...
call "%VSTOOLS%\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
if %ERRORLEVEL% neq 0 (
    echo [ERRORE] Impossibile configurare l'ambiente Visual Studio
    exit /b 1
)

:: Imposta i percorsi degli include e delle librerie
set "INCLUDE=%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\um;%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\shared;%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\ucrt;%VSTOOLS%\VC\Tools\MSVC\14.38.33130\include"
set "LIB=%WIN_SDK_ROOT%\Lib\%WIN_SDK_VERSION%\um\x64;%WIN_SDK_ROOT%\Lib\%WIN_SDK_VERSION%\ucrt\x64;%VSTOOLS%\VC\Tools\MSVC\14.38.33130\lib\x64"
set "PATH=%WIN_SDK_ROOT%\bin\%WIN_SDK_VERSION%\x64;%PATH%"

:: Creazione directory di output
echo [INFO] Creazione directory di output...
if not exist build mkdir build
if not exist build\obj mkdir build\obj

:: Compilazione assembly
echo [INFO] Inizio compilazione file assembly...

:: Lista dei file assembly da compilare
set ASM_FILES=interface.asm anti_debug.asm vbva_exploit.asm scsi_exploit.asm vram_exploit.asm

:: Compila ogni file assembly
for %%f in (%ASM_FILES%) do (
    echo [INFO] Assemblaggio %%f...
    "%NASM_EXE%" -f win64 -o build/obj/%%~nf.obj %%f
    if !ERRORLEVEL! neq 0 (
        echo [ERRORE] Assemblaggio %%f fallito
        exit /b 1
    )
    echo [SUCCESS] Assemblaggio %%f completato
)

:: Compilazione DLL
echo [INFO] Inizio compilazione DLL...
echo [INFO] Compilazione interface.dll...

:: Verifica che interface.c esista
if not exist interface.c (
    echo [ERRORE] File interface.c non trovato
    exit /b 1
)

:: Compila interface.c
cl.exe /nologo /c /O2 /GL /GS- /Gy /W3 /Gm- /EHsc /MT ^
    /I"%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\um" ^
    /I"%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\shared" ^
    /I"%WIN_SDK_ROOT%\Include\%WIN_SDK_VERSION%\ucrt" ^
    /I"%VSTOOLS%\VC\Tools\MSVC\14.38.33130\include" ^
    /Fo"build\obj\interface.obj" ^
    interface.c

if %ERRORLEVEL% neq 0 (
    echo [ERRORE] Compilazione interface.c fallita
    exit /b 1
)

:: Link DLL
link.exe /nologo /DLL /MACHINE:X64 /OPT:REF /OPT:ICF /LTCG ^
    /OUT:"build\spectre9.dll" ^
    /IMPLIB:"build\spectre9.lib" ^
    /LIBPATH:"%WIN_SDK_ROOT%\Lib\%WIN_SDK_VERSION%\um\x64" ^
    /LIBPATH:"%WIN_SDK_ROOT%\Lib\%WIN_SDK_VERSION%\ucrt\x64" ^
    /LIBPATH:"%VSTOOLS%\VC\Tools\MSVC\14.38.33130\lib\x64" ^
    /SUBSYSTEM:WINDOWS ^
    /DEBUG ^
    kernel32.lib user32.lib ntdll.lib ^
    build\obj\interface.obj ^
    build\obj\vbva_exploit.obj ^
    build\obj\scsi_exploit.obj ^
    build\obj\vram_exploit.obj ^
    build\obj\anti_debug.obj

if %ERRORLEVEL% neq 0 (
    echo [ERRORE] Linking interface.dll fallito
    exit /b 1
)

:: Copia la DLL nella posizione finale
echo [INFO] Copia DLL nella posizione finale...
copy /Y "build\spectre9.dll" "..\spectre9.dll"
if %ERRORLEVEL% neq 0 (
    echo [ERRORE] Copia DLL fallita
    exit /b 1
)

echo [SUCCESS] Build completata con successo
exit /b 0
