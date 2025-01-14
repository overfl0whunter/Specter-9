"""
Spectre-9 Virus Demo
Main entry point
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.welcome_message import WelcomeMessage
from gui.warning_dialog import WarningDialog
from gui.virus_button import VirusButton

def main():
    app = QApplication(sys.argv)
    
    # Mostra il messaggio di benvenuto
    welcome = WelcomeMessage()
    if welcome.exec_() == WelcomeMessage.Accepted:
        # Mostra il warning
        warning = WarningDialog()
        if warning.exec_() == WarningDialog.Accepted:
            # Mostra il pulsante finale
            button = VirusButton()
            if button.exec_() == VirusButton.Accepted:
                # TODO: Qui parte il virus
                print("Virus attivato!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
