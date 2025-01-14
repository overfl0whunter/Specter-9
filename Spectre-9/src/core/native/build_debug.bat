@echo off
setlocal enabledelayedexpansion

:: Aggiungi flag di debug
set DEBUG_FLAGS=/Zi /DEBUG /Od /MTd

:: Chiama lo script di build principale con i flag di debug
call build.bat %DEBUG_FLAGS%

:: Copia i file PDB nella directory finale
echo Copia file PDB...
copy /Y build\*.pdb ..\

echo Build debug completata!
