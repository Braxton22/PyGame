import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """ return true if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        # The alien is at the right edge if the right attribute of
        # its rect is greater than or equal to the right attribute of the screen’s rect
        if self.rect.right >= screen_rect.right:
            return True
        # It's at the left edge if its left value is less than or equal to 0
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ move the alien right or left """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x
