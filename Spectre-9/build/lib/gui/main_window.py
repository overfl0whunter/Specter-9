from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectre-9")
        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black;")
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Titolo
        title_label = QLabel("SPECTRE-9")
        title_label.setFont(QFont("Terminal", 48, QFont.Bold))
        title_label.setStyleSheet("color: #00ff00;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Sottotitolo
        subtitle_label = QLabel("Created by SeregonWar")
        subtitle_label.setFont(QFont("Terminal", 14))
        subtitle_label.setStyleSheet("color: #00ff00;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Separatore
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #00ff00;")
        layout.addWidget(separator)
        
        # Bottoni
        buttons = [
            ("Matrix Effect", self.not_implemented),
            ("File Explorer Chaos", self.not_implemented),
            ("Desktop Takeover", self.not_implemented),
            ("System Messages", self.not_implemented),
            ("Full Virus Experience", self.not_implemented),
            ("Exit", self.close)
        ]
        
        for text, callback in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Terminal", 14))
            button.setFixedSize(400, 60)
            button.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #003300;
                }
                QPushButton:pressed {
                    background-color: #006600;
                }
            """)
            button.clicked.connect(callback)
            layout.addWidget(button, alignment=Qt.AlignCenter)
        
        # Versione
        version_label = QLabel("v1.0.0")
        version_label.setFont(QFont("Terminal", 10))
        version_label.setStyleSheet("color: #00ff00;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Timer per l'effetto di glitch
        self.glitch_timer = QTimer()
        self.glitch_timer.timeout.connect(self.glitch_effect)
        self.glitch_timer.start(5000)  # Ogni 5 secondi
    
    def not_implemented(self):
        # TODO: Implementare le funzionalità
        pass
    
    def glitch_effect(self):
        # TODO: Aggiungere effetto glitch
        pass
    
    def keyPressEvent(self, event):
        # Chiudi con ESC
        if event.key() == Qt.Key_Escape:
            self.close()
