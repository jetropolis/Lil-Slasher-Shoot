import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):
    """A class to represent a single zombie in the horde"""

    def __init__(self, ai_settings, screen):
        """Initialize the zombie and set its starting position"""
        super(Zombie, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the zombie image and set its rect attribute
        self.image = pygame.image.load('images/zombie.bmp')
        self.rect = self.image.get_rect()

        #Start each new zombie near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the zombie's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the zombie at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if zombie is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        """Move the zombie right or left"""
        self.x += (self.ai_settings.zombie_speed_factor * self.ai_settings.horde_direction)
        self.rect.x = self.x