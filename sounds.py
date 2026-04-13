import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 1. Defensive "Dummy" for silent mode
class DummySound:
    def play(self): pass
    def stop(self): pass
    def set_volume(self, vol): pass
    def get_busy(self): return False

class SoundManager:
    def __init__(self):
        # Start with dummy sounds
        self.warp = DummySound()
        self.shoot = DummySound()
        self.powerup = DummySound()
        self.explosion = DummySound()
        self.audio_available = False

    def load_assets(self):
        """Called AFTER pygame.init() in main.py"""
        if pygame.mixer.get_init():
            try:
                self.warp = pygame.mixer.Sound(resource_path("assets/playerwarp.wav"))
                self.shoot = pygame.mixer.Sound(resource_path("assets/playershoot.wav"))
                self.powerup = pygame.mixer.Sound(resource_path("assets/powerUp.wav"))
                self.explosion = pygame.mixer.Sound(resource_path("assets/asteroidexplosion.wav"))
                
                self.warp.set_volume(0.4)
                self.shoot.set_volume(0.2)
                self.explosion.set_volume(0.4)
                self.audio_available = True
                print("Audio assets loaded successfully.")
            except pygame.error as e:
                print(f"Warning: Files found but could not load sounds: {e}")
        else:
            print("Warning: Mixer not initialized. Running in silent mode.")

# Single global instance
sounds = SoundManager()