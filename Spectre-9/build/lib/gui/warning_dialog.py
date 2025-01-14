from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                             QCheckBox, QPushButton, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class WarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ATTENZIONE - VIRUS DIMOSTRATIVO")
        self.setFixedSize(800, 600)  # Aumentata la dimensione
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: black;
            }
            QLabel {
                color: #00ff00;
                margin: 10px;
            }
            QLabel#warning {
                color: #ff0000;
                font-weight: bold;
                padding: 20px;
            }
        """)
        
        # Layout principale
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Aumentato lo spazio tra gli elementi
        layout.setContentsMargins(40, 40, 40, 40)  # Aumentati i margini
        self.setLayout(layout)
        
        # Titolo di avvertimento
        warning_label = QLabel("! QUESTO E' UN VIRUS DIMOSTRATIVO !")  # Rimosso caratteri speciali
        warning_label.setObjectName("warning")
        warning_label.setFont(QFont("Terminal", 16, QFont.Bold))
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)
        
        # Spazio dopo il titolo
        layout.addSpacing(20)
        
        # Testo informativo
        info_text = (
            "Questo e' un virus creato esclusivamente per scopi dimostrativi\n"
            "come parte della serie YouTube \"Virus Saga\".\n"
            "\n"
            "AVVERTIMENTI IMPORTANTI:\n"
            "* Questo e' un vero virus che puo' danneggiare il tuo sistema\n"
            "* Eseguilo SOLO in una macchina virtuale (VM)\n"
            "* NON eseguirlo sul tuo computer principale\n"
            "* NON distribuirlo o condividerlo con altri\n"
            "* Usalo solo per scopi educativi e dimostrativi\n"
            "\n"
            "Creato per: Virus Saga YouTube Series\n"
            "Data di creazione: 14/01/2025"
        )
        
        info_label = QLabel(info_text)
        info_label.setFont(QFont("Terminal", 12))
        info_label.setAlignment(Qt.AlignLeft)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Spazio prima della checkbox
        layout.addSpacing(20)
        
        # Checkbox di conferma
        self.confirm_checkbox = QCheckBox(
            "Confermo di essere consapevole dei rischi e di utilizzare una VM"
        )
        self.confirm_checkbox.setFont(QFont("Terminal", 12))
        self.confirm_checkbox.setStyleSheet("""
            QCheckBox {
                color: #00ff00;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #00ff00;
                background: black;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00ff00;
                background: #00ff00;
            }
        """)
        layout.addWidget(self.confirm_checkbox)
        
        # Spazio elastico prima dei pulsanti
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Pulsante Procedi
        self.proceed_button = QPushButton("Procedi")
        self.proceed_button.setFont(QFont("Terminal", 14))
        self.proceed_button.setFixedSize(300, 50)  # Pulsante più largo
        self.proceed_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: #ff0000;
                border: 2px solid #ff0000;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #330000;
            }
            QPushButton:pressed {
                background-color: #660000;
            }
        """)
        self.proceed_button.clicked.connect(self.proceed)
        layout.addWidget(self.proceed_button, alignment=Qt.AlignCenter)
        
        # Pulsante Esci
        self.exit_button = QPushButton("Esci")
        self.exit_button.setFont(QFont("Terminal", 14))
        self.exit_button.setFixedSize(300, 50)  # Pulsante più largo
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #003300;
            }
            QPushButton:pressed {
                background-color: #006600;
            }
        """)
        self.exit_button.clicked.connect(self.reject)
        layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)
        
        # Spazio finale
        layout.addSpacing(20)
    
    def proceed(self):
        if not self.confirm_checkbox.isChecked():
            msg = QMessageBox(self)  # Imposta il parent
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Errore")
            msg.setText("Devi confermare di essere consapevole dei rischi e di utilizzare una VM!")
            msg.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)  # Forza in primo piano
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: black;
                }
                QMessageBox QLabel {
                    color: #00ff00;
                    font-family: Terminal;
                    font-size: 12px;
                    padding: 20px;
                }
                QPushButton {
                    background-color: black;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 5px;
                    padding: 10px;
                    min-width: 100px;
                    font-family: Terminal;
                }
                QPushButton:hover {
                    background-color: #003300;
                }
            """)
            msg.exec_()
            return
        
        confirm_msg = QMessageBox(self)  # Imposta il parent
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setWindowTitle("Conferma Finale")
        confirm_msg.setText("Sei ASSOLUTAMENTE SICURO di voler procedere?\n\n" +
                          "Questo è l'ultimo avvertimento prima dell'esecuzione del virus.")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setDefaultButton(QMessageBox.No)
        confirm_msg.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)  # Forza in primo piano
        confirm_msg.setStyleSheet("""
            QMessageBox {
                background-color: black;
            }
            QMessageBox QLabel {
                color: #00ff00;
                font-family: Terminal;
                font-size: 12px;
                padding: 20px;
            }
            QPushButton {
                background-color: black;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
                font-family: Terminal;
            }
            QPushButton:hover {
                background-color: #003300;
            }
        """)
        
        if confirm_msg.exec_() == QMessageBox.Yes:
            self.accept()
    
    def keyPressEvent(self, event):
        # Ignora il tasto ESC
        if event.key() == Qt.Key_Escape:
            return
        super().keyPressEvent(event)
