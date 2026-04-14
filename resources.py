import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# A dictionary to store our images in memory
CARD_IMAGES = {}

def load_card_assets():
    suits = ["hearts", "diamonds", "clubs", "spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    # Load every card into the dictionary
    for suit in suits:
        for rank in ranks:
            relative_file = f"assets/cards/{suit}_{rank}.png"
            file_path = resource_path(relative_file)
            # Load and convert for better performance
            img = pygame.image.load(file_path).convert_alpha()
            # If 64x64 is too small or large, scale it here!
            img = pygame.transform.scale(img, (100, 140))
            CARD_IMAGES[f"{suit}_{rank}"] = img
            
    # Don't forget the back of the card!
    back_path = resource_path("assets/cards/card_back.png")
    CARD_IMAGES["back"] = pygame.image.load(back_path).convert_alpha()
    CARD_IMAGES["back"] = pygame.transform.scale(CARD_IMAGES["back"], (100,140))