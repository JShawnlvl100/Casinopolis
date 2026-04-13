import pygame
import random
from resources import CARD_IMAGES

class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit, start_pos, target_pos):
        super().__init__(self.containers)
        self.rank = rank
        self.suit = suit
        self.face_up = False # Start face down while moving?
        
        # Initial setup
        self.image = CARD_IMAGES["back"]
        self.rect = self.image.get_rect(center=start_pos)
        
        # Movement logic
        self.target_pos = pygame.Vector2(target_pos)
        self.position = pygame.Vector2(start_pos)
        self.speed = 1200 # Pixels per second

    def update(self, dt):
        # Calculate the vector to the target
        move_vector = self.target_pos - self.position
        distance = move_vector.length()

        if distance > 0:
            # Move towards target
            direction = move_vector.normalize()
            move_amount = self.speed * dt
            
            # Don't overshoot the target
            if move_amount > distance:
                self.position = self.target_pos
                self.on_reach_target()
            else:
                self.position += direction * move_amount
            
            self.rect.center = self.position

    def on_reach_target(self):
        # Flip the card over when it arrives!
        self.face_up = True
        self.image = CARD_IMAGES[f"{self.suit}_{self.rank}"]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def flip(self):
        self.face_up = True
        # Swap the placeholder/back image for the real one
        self.image = CARD_IMAGES[f"{self.suit}_{self.rank}"]

