import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py
from setuptools.command.install import install
from distutils.command.clean import clean

class BuildNativeCommand(Command):
    description = 'Build native DLL components'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Ottieni il percorso assoluto della directory del progetto
        project_root = os.path.abspath(os.path.dirname(__file__))
        
        # Directory contenente il codice nativo
        native_dir = os.path.join(project_root, 'src', 'core', 'native')
        build_script = os.path.join(native_dir, 'build.bat')
        
        print(f"[INFO] Directory nativa: {native_dir}")
        print(f"[INFO] Script di build: {build_script}")
        
        if not os.path.exists(build_script):
            print(f"[ERRORE] build.bat non trovato in: {build_script}")
            raise FileNotFoundError(f"build.bat non trovato in: {build_script}")

        # Esegui il build script
        try:
            print(f"[INFO] Esecuzione di {build_script} in {native_dir}")
            result = subprocess.run([build_script], 
                                 cwd=native_dir, 
                                 shell=True, 
                                 capture_output=True, 
                                 text=True)
            
            # Stampa l'output del processo
            if result.stdout:
                print("[BUILD OUTPUT]")
                print(result.stdout)
            
            if result.stderr:
                print("[BUILD ERRORS]")
                print(result.stderr)
            
            result.check_returncode()
            
        except subprocess.CalledProcessError as e:
            print(f"[ERRORE] Compilazione fallita con codice {e.returncode}")
            print(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
            raise

class CustomBuildPy(build_py):
    def run(self):
        self.run_command('build_native')
        build_py.run(self)

        # Copia logo.ico nella directory di build
        project_root = os.path.abspath(os.path.dirname(__file__))
        src_ico = os.path.join(project_root, 'src', 'assets', 'logo.ico')
        if os.path.exists(src_ico):
            dst_ico = os.path.join(self.build_lib, 'assets', 'logo.ico')
            os.makedirs(os.path.dirname(dst_ico), exist_ok=True)
            shutil.copy2(src_ico, dst_ico)
            print(f"[INFO] Copiato {src_ico} in {dst_ico}")
        else:
            print(f"[WARNING] File logo.ico non trovato in: {src_ico}")

        # Copia main.py nella directory di build
        src_main = os.path.join(project_root, 'src', 'main.py')
        if os.path.exists(src_main):
            dst_main = os.path.join(self.build_lib, 'main.py')
            shutil.copy2(src_main, dst_main)
            print(f"[INFO] Copiato {src_main} in {dst_main}")
        else:
            print(f"[WARNING] File main.py non trovato in: {src_main}")

class CustomInstall(install):
    def run(self):
        self.run_command('build_native')
        install.run(self)

class CustomClean(clean):
    def run(self):
        project_root = os.path.abspath(os.path.dirname(__file__))
        
        # Pulisci i file di build nativi
        native_build_dir = os.path.join(project_root, 'src', 'core', 'native', 'build')
        if os.path.exists(native_build_dir):
            shutil.rmtree(native_build_dir)
            print(f"[INFO] Rimossa directory {native_build_dir}")

        # Pulisci la DLL compilata
        dll_path = os.path.join(project_root, 'src', 'core', 'spectre9.dll')
        if os.path.exists(dll_path):
            os.remove(dll_path)
            print(f"[INFO] Rimosso file {dll_path}")

        clean.run(self)

# Verifica che tutti i file necessari esistano
def verify_required_files():
    project_root = os.path.abspath(os.path.dirname(__file__))
    required_files = [
        os.path.join(project_root, 'src', 'core', 'native', 'build.bat'),
        os.path.join(project_root, 'src', 'assets', 'logo.ico'),
        os.path.join(project_root, 'src', 'main.py'),
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("[ERRORE] File richiesti mancanti:")
        for f in missing_files:
            print(f"  - {f}")
        raise FileNotFoundError("File richiesti mancanti")

# Verifica i file prima del setup
verify_required_files()

setup(
    name="spectre9",
    version="1.0.0",
    author="Marco",
    description="Spectre-9 Virus Demo",
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    packages=find_packages(where="src") + ['core.native'],
    package_dir={"": "src"},
    py_modules=['main'],  # Includi main.py come modulo
    include_package_data=True,
    package_data={
        'core.native': ['*.dll', '*.asm', '*.inc', '*.h', '*.c', '*.bat'],
        'assets': ['*.ico'],
    },
    install_requires=[
        'PyQt5>=5.15.0',
        'psutil>=5.8.0',  # Per ProcessInjector
        'pywin32>=228',   # Per accesso a Windows API
        'typing>=3.7.4',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'spectre9=main:main',
        ],
    },
    cmdclass={
        'build_native': BuildNativeCommand,
        'build_py': CustomBuildPy,
        'install': CustomInstall,
        'clean': CustomClean,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Assembly',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
