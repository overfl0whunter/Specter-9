from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VirusButton(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spectre-9")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")
        
        # Layout principale
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)
        
        # Pulsante Cliccami
        self.virus_button = QPushButton("CLICCAMI")
        self.virus_button.setFont(QFont("Terminal", 20, QFont.Bold))
        self.virus_button.setFixedSize(300, 200)
        self.virus_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: #ff0000;
                border: 3px solid #ff0000;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #330000;
                border-width: 4px;
            }
            QPushButton:pressed {
                background-color: #660000;
                border-width: 5px;
            }
        """)
        self.virus_button.clicked.connect(self.accept)
        layout.addWidget(self.virus_button, alignment=Qt.AlignCenter)
    
    def keyPressEvent(self, event):
        # Ignora il tasto ESC
        if event.key() == Qt.Key_Escape:
            return
        super().keyPressEvent(event)
