# Spectre-9 Virus Demo

Un dimostratore di exploit per VirtualBox che combina assembly e Python.

## Requisiti di Sistema

- Windows 10/11
- Python 3.7 o superiore
- Visual Studio 2022 Build Tools
- NASM (Netwide Assembler)
- Windows SDK 10.0.22621.0 o superiore

## Installazione

### 1. Prerequisiti

Assicurati di avere installato:

```bash
# Installa le dipendenze Python
pip install PyQt5 psutil pywin32
```

### 2. Installazione NASM

1. Scarica NASM da [nasm.us](https://www.nasm.us/)
2. Installa in `C:\NASM`
3. Aggiungi `C:\NASM` al PATH di sistema

### 3. Visual Studio Build Tools

1. Scarica Visual Studio 2022 Build Tools
2. Durante l'installazione, seleziona:
   - C++ build tools
   - Windows SDK 10.0.22621.0

### 4. Installazione del Progetto

#### Modalità Sviluppo (Consigliata)

```bash
# Clona il repository
git clone https://github.com/tuouser/Spectre-9.git
cd Spectre-9

# Installa in modalità sviluppo
pip install -e .
```

#### Installazione Globale

```bash
# Richiede privilegi di amministratore
python setup.py install
```

## Utilizzo

```bash
# Avvia il programma
spectre9
```

## Struttura del Progetto

```
Spectre-9/
├── src/
│   ├── assets/           # File di risorse (icone, immagini)
│   ├── core/            
│   │   ├── native/      # Codice assembly e C
│   │   └── *.py         # Core Python
│   ├── effects/         # Effetti visivi
│   ├── gui/            # Interfaccia utente
│   └── utils/          # Utilità varie
├── setup.py            # Script di installazione
└── README.md          # Questo file
```

## Sviluppo

### Build Manuale

```bash
# Compila solo la DLL
cd src/core/native
./build.bat

# Build completa
python setup.py clean --all
python setup.py build
```

### Pulizia

```bash
python setup.py clean --all
```

## Note di Sicurezza

⚠️ **ATTENZIONE**: Questo è un progetto dimostrativo. Non utilizzare in ambienti di produzione.

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
