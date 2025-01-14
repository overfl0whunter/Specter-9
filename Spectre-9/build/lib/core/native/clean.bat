@echo off
echo Pulizia dei file di build...

:: Rimuovi directory build
if exist build (
    rd /s /q build
    echo Directory build rimossa
)

:: Rimuovi DLL compilate
del /f /q *.dll
echo DLL rimosse

:: Rimuovi altri file temporanei
del /f /q *.obj
del /f /q *.exp
del /f /q *.lib
echo File temporanei rimossi

echo Pulizia completata!
