# Import Modules
import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard

# Create an empty pygame window which we can later put game elements into
def run_game():

    # Initialize pygame, settings and create a screen object
    pygame.init()
    ai_settings = Settings()

    # screen is a surface, which is a part of the screen where you display a game element. Each element in the game is a surface. Surface is automatically redrawn on every pass through the loop
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard
    stats = Gamestats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a Ship
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in
    bullets = Group()

    # Make a group of aliens
    aliens = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the man loop for the game
    while True:
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )


run_game()
