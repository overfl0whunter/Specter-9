# Build System per Componenti Nativi

Questo sistema di build compila tutti i componenti nativi (DLL e assembly) del progetto Spectre-9.

## Prerequisiti

1. **NASM (Netwide Assembler)**
   - Scarica da: https://www.nasm.us/
   - Installa in: `C:\NASM`
   - Aggiungi al PATH di sistema

2. **Visual Studio Build Tools**
   - Installa Visual Studio 2022 con C++ build tools
   - Richiesti: MSVC e Windows SDK

## Script Disponibili

### build.bat
Script principale di build. Compila tutti i componenti:
- Assembla i file .asm in oggetti
- Compila le DLL
- Copia i file nella directory corretta

### build_debug.bat
Versione debug del build che include:
- Simboli di debug
- Ottimizzazioni disabilitate
- File PDB per il debugging

### clean.bat
Pulisce i file di build:
- Rimuove la directory build
- Elimina file temporanei
- Rimuove DLL compilate

## Struttura Output

```
build/
├── obj/            # File oggetto (.obj)
│   ├── interface.obj
│   ├── anti_debug.obj
│   └── ...
├── interface.dll   # DLL compilate
├── anti_debug.dll
└── ...
```

## Utilizzo

1. Compila release:
```batch
build.bat
```

2. Compila debug:
```batch
build_debug.bat
```

3. Pulisci:
```batch
clean.bat
```

## Troubleshooting

1. **NASM non trovato**
   - Verifica installazione in C:\NASM
   - Controlla PATH di sistema

2. **Visual Studio Build Tools mancanti**
   - Installa/ripara Visual Studio
   - Verifica componenti C++

3. **Errori di linking**
   - Verifica percorsi LIB
   - Controlla dipendenze DLL
