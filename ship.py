import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        # initialize the ship and set its starting position
        # super makes sure that ship inherits from sprite
        super(Ship, self).__init__()
        self.screen = screen

        self.ai_settings = ai_settings

        # load the ship image and get its rect
        # Rects are rectangles. They are efficient because rectangles are simple geometric shapes.
        # you can use x/y coordinates at the top, bottom, left and right edges of the rectangle as well as the center.
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        # center, centerx and centery for elements
        # top, bottom, left or right when working with screen edges
        # origin is at top left and you work down/right from there
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement Flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Update the ship's position based on movement flags
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.center = self.screen_rect.centerx