"""
Effetti visivi e sonori del virus
"""
import random
import pygame
import win32gui
import win32con
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

class VisualEffects:
    def __init__(self):
        # Inizializza pygame per gli effetti sonori
        pygame.mixer.init()
        self.sounds = {
            'glitch': pygame.mixer.Sound('assets/sounds/glitch.wav'),
            'error': pygame.mixer.Sound('assets/sounds/error.wav'),
            'warning': pygame.mixer.Sound('assets/sounds/warning.wav')
        }
        
    def play_sound(self, sound_name):
        """Riproduce un effetto sonoro"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
class ScreenGlitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        
        # Timer per gli effetti glitch
        self.glitch_timer = QTimer()
        self.glitch_timer.timeout.connect(self.update)
        self.glitch_timer.start(50)  # Aggiorna ogni 50ms
        
        # Parametri glitch
        self.glitch_intensity = 0
        self.glitch_lines = []
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Crea linee glitch casuali
        self.glitch_lines = []
        for _ in range(int(self.glitch_intensity * 10)):
            y = random.randint(0, self.height())
            width = random.randint(50, 200)
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(100, 200)
            )
            self.glitch_lines.append((y, width, color))
            
        # Disegna le linee glitch
        for y, width, color in self.glitch_lines:
            painter.fillRect(0, y, width, 2, color)
            
    def set_intensity(self, value):
        """Imposta l'intensità dell'effetto glitch (0-1)"""
        self.glitch_intensity = max(0, min(1, value))
        
class ScreenDistortion:
    def __init__(self):
        self.screen_width = win32gui.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32gui.GetSystemMetrics(win32con.SM_CYSCREEN)
        
    def create_distortion(self, intensity=0.5):
        """Crea un effetto di distorsione dello schermo"""
        # Crea un'immagine vuota
        image = Image.new('RGBA', (self.screen_width, self.screen_height), (0,0,0,0))
        draw = ImageDraw.Draw(image)
        
        # Aggiungi effetti di distorsione
        for _ in range(int(intensity * 100)):
            x1 = random.randint(0, self.screen_width)
            y1 = random.randint(0, self.screen_height)
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(-50, 50)
            
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(50, 150)
            )
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
            
        # Applica blur per un effetto più smooth
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        
        return image
