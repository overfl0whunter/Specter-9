import tkinter as tk
from tkinter import ttk
import sys

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spectre-9 - Menu Principale")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        
        # Forza la finestra in primo piano
        self.root.lift()
        self.root.attributes('-topmost', True)
        
        # Frame principale
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Stile per i bottoni
        style = ttk.Style()
        style.configure(
            'Custom.TButton',
            background='black',
            foreground='#00ff00',
            font=('Terminal', 12),
            padding=10
        )
        
        # Titolo
        self.title_label = tk.Label(
            self.main_frame,
            text="SPECTRE-9",
            font=('Terminal', 48, 'bold'),
            fg='#00ff00',
            bg='black'
        )
        self.title_label.pack(pady=(0, 50))
        
        # Sottotitolo
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Created by SeregonWar",
            font=('Terminal', 14),
            fg='#00ff00',
            bg='black'
        )
        self.subtitle_label.pack(pady=(0, 50))
        
        # Frame per i bottoni
        button_frame = tk.Frame(self.main_frame, bg='black')
        button_frame.pack(expand=True)
        
        # Lista dei bottoni
        buttons = [
            ("Matrix Effect", self.not_implemented),
            ("File Explorer Chaos", self.not_implemented),
            ("Desktop Takeover", self.not_implemented),
            ("System Messages", self.not_implemented),
            ("Full Virus Experience", self.not_implemented),
            ("Exit", self.exit_program)
        ]
        
        # Creazione bottoni
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Terminal', 14),
                fg='#00ff00',
                bg='black',
                activebackground='#003300',
                activeforeground='#00ff00',
                width=30,
                height=2,
                relief=tk.RIDGE,
                bd=2
            )
            btn.pack(pady=10)
        
        # Versione
        version_label = tk.Label(
            self.main_frame,
            text="v1.0.0",
            font=('Terminal', 10),
            fg='#00ff00',
            bg='black'
        )
        version_label.pack(side='bottom', pady=10)
        
        # Tasto ESC per uscire
        self.root.bind('<Escape>', lambda e: self.exit_program())
        
        self.root.mainloop()
    
    def not_implemented(self):
        popup = tk.Toplevel(self.root)
        popup.title("Info")
        popup.geometry("300x100")
        popup.configure(bg='black')
        
        # Centra il popup
        popup.geometry(f"+{self.root.winfo_x() + 500}+{self.root.winfo_y() + 300}")
        
        label = tk.Label(
            popup,
            text="Funzionalità in arrivo...",
            font=('Terminal', 12),
            fg='#00ff00',
            bg='black'
        )
        label.pack(expand=True)
        
        # Chiudi automaticamente dopo 2 secondi
        popup.after(2000, popup.destroy)
    
    def exit_program(self):
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    MainMenu()
