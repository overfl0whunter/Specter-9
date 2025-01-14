"""
Sistema delle quest e gestione della trama
"""
import os
import random
import time
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class Quest:
    def __init__(self, title, description, time_limit, files_to_find=None):
        self.title = title
        self.description = description
        self.time_limit = time_limit  # in secondi
        self.files_to_find = files_to_find or []
        self.completed = False
        self.failed = False
        
class QuestSystem:
    def __init__(self):
        self.quests = [
            Quest(
                "Inizializzazione Sistema",
                "Il virus sta prendendo il controllo del sistema.\nTrova il file 'antivirus.exe' per fermarlo!",
                120,  # 2 minuti
                ["antivirus.exe"]
            ),
            Quest(
                "Corruzione in Corso",
                "I tuoi file stanno per essere criptati.\nTrova la chiave di decriptazione in 'decrypt_key.txt'!",
                180,  # 3 minuti
                ["decrypt_key.txt"]
            ),
            Quest(
                "Fuga dalla VM",
                "Il virus sta cercando di evadere dalla VM.\nTrova e elimina 'escape_vector.sys'!",
                240,  # 4 minuti
                ["escape_vector.sys"]
            )
        ]
        self.current_quest = 0
        self.total_time = sum(quest.time_limit for quest in self.quests)
        self.time_remaining = self.total_time
        
    def show_quest_dialog(self, quest):
        """Mostra il dialogo della quest corrente"""
        dialog = QDialog()
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        dialog.setStyleSheet("background-color: black;")
        dialog.setFixedSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Titolo
        title = QLabel(quest.title)
        title.setFont(QFont("Terminal", 16, QFont.Bold))
        title.setStyleSheet("color: #ff0000;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Descrizione
        desc = QLabel(quest.description)
        desc.setFont(QFont("Terminal", 12))
        desc.setStyleSheet("color: #00ff00;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Timer
        self.timer_label = QLabel(f"Tempo rimanente: {self.time_remaining}s")
        self.timer_label.setFont(QFont("Terminal", 14))
        self.timer_label.setStyleSheet("color: #ff0000;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)
        
        dialog.setLayout(layout)
        dialog.show()
        return dialog
        
    def start_quest(self):
        """Avvia la quest corrente"""
        if self.current_quest >= len(self.quests):
            return False
            
        quest = self.quests[self.current_quest]
        dialog = self.show_quest_dialog(quest)
        
        # Timer per aggiornare il tempo rimanente
        timer = QTimer()
        timer.timeout.connect(lambda: self.update_timer(dialog))
        timer.start(1000)  # Aggiorna ogni secondo
        
        return True
        
    def update_timer(self, dialog):
        """Aggiorna il timer della quest"""
        self.time_remaining -= 1
        if hasattr(self, 'timer_label'):
            self.timer_label.setText(f"Tempo rimanente: {self.time_remaining}s")
            
        if self.time_remaining <= 0:
            dialog.close()
            self.game_over()
            
    def check_quest_completion(self):
        """Verifica se la quest corrente è stata completata"""
        quest = self.quests[self.current_quest]
        
        # Verifica se i file necessari sono stati trovati/eliminati
        all_files_found = True
        for file in quest.files_to_find:
            if os.path.exists(file):
                all_files_found = False
                break
                
        if all_files_found:
            quest.completed = True
            self.current_quest += 1
            return True
            
        return False
        
    def game_over(self):
        """Gestisce la fine del gioco"""
        msg = QMessageBox()
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("GAME OVER")
        msg.setText("Il tempo è scaduto!\nLa VM verrà distrutta!")
        msg.setIcon(QMessageBox.Critical)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: black;
            }
            QMessageBox QLabel {
                color: #ff0000;
                font-family: Terminal;
                font-size: 14px;
            }
        """)
        msg.exec_()
