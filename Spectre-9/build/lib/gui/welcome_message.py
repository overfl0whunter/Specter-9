from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class WelcomeMessage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Messaggio")
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")
        
        # Layout principale
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Messaggio
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Terminal", 14))
        self.message_label.setStyleSheet("color: #00ff00;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # Firma
        self.signature_label = QLabel("Created by SeregonWar")
        self.signature_label.setFont(QFont("Terminal", 12))
        self.signature_label.setStyleSheet("color: #00ff00;")
        self.signature_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.signature_label)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 5px;
                text-align: center;
                background-color: black;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
        """)
        layout.addWidget(self.progress)
        
        # Pulsante Procedi (inizialmente nascosto)
        self.proceed_button = QPushButton("Procedi")
        self.proceed_button.setFont(QFont("Terminal", 14))
        self.proceed_button.setFixedSize(200, 50)
        self.proceed_button.setStyleSheet("""
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
        self.proceed_button.clicked.connect(self.accept)
        self.proceed_button.hide()  # Nascosto inizialmente
        layout.addWidget(self.proceed_button, alignment=Qt.AlignCenter)
        
        # Messaggio completo
        self.full_message = """Ciao NFire,

ti seguo da parecchio e volevo creare un virus da inviarti.
Dopo mesi di ragionamento e miglioramento ho creato questo,
ti affido la mia creazione!

(ci tengo a salutare tutti gli spettatori che stanno guardando il video)

- SeregonWar"""
        
        # Calcola il numero totale di caratteri
        self.total_chars = len(self.full_message)
        
        # Timer per l'effetto typewriter
        self.current_char = 0
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self.update_text_and_progress)
        self.type_timer.start(30)  # 30ms tra ogni carattere
        
    def update_text_and_progress(self):
        if self.current_char < self.total_chars:
            # Aggiorna il testo
            current_text = self.full_message[:self.current_char + 1]
            self.message_label.setText(current_text)
            
            # Aggiorna la progress bar in base alla percentuale di testo mostrato
            progress = (self.current_char + 1) / self.total_chars * 100
            self.progress.setValue(int(progress))
            
            self.current_char += 1
        else:
            self.type_timer.stop()
            # Nascondi la progress bar e mostra il pulsante
            self.progress.hide()
            self.proceed_button.show()
    
    def keyPressEvent(self, event):
        # Ignora il tasto ESC per forzare l'utente a vedere il messaggio
        if event.key() == Qt.Key_Escape:
            return
        super().keyPressEvent(event)
