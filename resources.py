import pygame
import os

# A dictionary to store our images in memory
CARD_IMAGES = {}

def load_card_assets():
    suits = ["hearts", "diamonds", "clubs", "spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
    
    # Load every card into the dictionary
    for suit in suits:
        for rank in ranks:
            file_path = os.path.join("assets", "images", "cards", f"{suit}_{rank}.png")
            # Load and convert for better performance
            img = pygame.image.load(file_path).convert_alpha()
            # If 64x64 is too small or large, scale it here!
            # img = pygame.transform.scale(img, (100, 140))
            CARD_IMAGES[f"{suit}_{rank}"] = img
            
    # Don't forget the back of the card!
    back_path = os.path.join("assets", "images", "cards", "card_back.png")
    CARD_IMAGES["back"] = pygame.image.load(back_path).convert_alpha()