import pygame

# the bullet class inherits from Sprite, which we import from the pygame.sprite module.
# when you use sprites, you can group related elements in your game and act on all the grouped elements at once
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        # create a bullet object at the ship's current position
        # super makes sure bullet inherits properly from Sprite
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rectangle at (0,0) and then set the correct position
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # move the bullet up the screen
        # update the decimal position of the bullet
        # its a subtraction because the origin is at the top left, so in order to move it upwards, you gotta decrease the y position
        self.y -= self.speed_factor
        # update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
