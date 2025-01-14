import tkinter as tk
from tkinter import ttk
import time
import threading
from effects.main_menu import MainMenu

class WelcomeScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spectre-9")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        
        # Forza la finestra in primo piano
        self.root.lift()
        self.root.attributes('-topmost', True)
        
        # Frame principale
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(expand=True, fill='both')
        
        # Logo o titolo animato
        self.title_label = tk.Label(
            self.main_frame,
            text="SPECTRE-9",
            font=('Terminal', 48, 'bold'),
            fg='#00ff00',
            bg='black'
        )
        self.title_label.pack(pady=50)
        
        # Messaggio principale con effetto typewriter
        self.message_label = tk.Label(
            self.main_frame,
            text="",
            font=('Consolas', 14),
            fg='#00ff00',
            bg='black',
            wraplength=800,
            justify='center'
        )
        self.message_label.pack(pady=30)
        
        # Firma
        self.signature_label = tk.Label(
            self.main_frame,
            text="Created by SeregonWar",
            font=('Terminal', 12),
            fg='#00ff00',
            bg='black'
        )
        self.signature_label.pack(side='bottom', pady=20)
        
        # Loading bar
        self.progress_frame = tk.Frame(self.main_frame, bg='black')
        self.progress_frame.pack(side='bottom', pady=50)
        
        self.progress = ttk.Progressbar(
            self.progress_frame,
            length=400,
            mode='determinate',
            style='Green.Horizontal.TProgressbar'
        )
        self.progress.pack()
        
        # Configura stile della progress bar
        style = ttk.Style()
        style.configure(
            'Green.Horizontal.TProgressbar',
            troughcolor='black',
            background='#00ff00'
        )
        
        # Messaggio da mostrare con effetto typewriter
        self.full_message = """Ciao NFire,
ti seguo da parecchio e volevo creare un virus da inviarti.
Dopo mesi di ragionamento e miglioramento ho creato questo,
ti affido la mia creazione!

(ci tengo a salutare tutti gli spettatori che stanno guardando il video)

- SeregonWar"""
        
        # Avvia gli effetti
        self.start_effects()
        
        # Tasto ESC per uscire
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        self.root.mainloop()
    
    def typewriter_effect(self):
        delay = 50  # millisecondi tra ogni carattere
        current_text = ""
        
        for char in self.full_message:
            current_text += char
            self.message_label.config(text=current_text)
            self.root.update()
            time.sleep(delay/1000)
    
    def progress_animation(self):
        for i in range(101):
            self.progress['value'] = i
            self.root.update()
            time.sleep(0.05)
        
        # Dopo il caricamento, aspetta un momento e poi procedi
        time.sleep(1)
        self.root.destroy()
        # Avvia il menu principale
        MainMenu()
    
    def start_effects(self):
        # Avvia l'effetto typewriter in un thread separato
        threading.Thread(target=self.typewriter_effect, daemon=True).start()
        # Avvia l'animazione della progress bar in un thread separato
        threading.Thread(target=self.progress_animation, daemon=True).start()

if __name__ == "__main__":
    WelcomeScreen()
