import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Respond to key presses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # respond to key presses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )

        # Identify there is a keydown
        elif event.type == pygame.KEYDOWN:
            # Identify the key pressed was the right arrow key
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        # Identify there is a key up
        elif event.type == pygame.KEYUP:
            # If the event was a key right, stop moving the ship
            check_keyup_events(event, ship)


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    # fire a bullet if the limit isn't reached yet
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets
):
    """respond to bullet-alien collisions"""
    # check for any bullets that have hit aliens. If so, get rid of the bullet and the alien
    """The two True arguments tell Pygame whether to delete
    the bullets and aliens that have collided. (To make a high-powered bullet
    that’s able to travel to the top of the screen, destroying every alien in its
    path, you could set the first Boolean argument to False and keep the second
    Boolean argument set to True. The aliens hit would disappear, but all bullets
    would stay active until they disappeared off the top of the screen.)"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    """ any bullet that collides with an alien becomes a key in the collisions dictionary. The value associated with
    each bullet is a list of aliens it has collided with. This loop is looping through the collisions dictionary to make 
    sure we award points for each alien hit:"""
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet. Start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # Increase level
        stats.level += 1
        sb.prep_level()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # update the position of bullets and get rid of old bullets
    bullets.update()
    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    # This creates a margin equal to the width of one alien. Two margins, one on the right and the left
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # the space needed to display an alien is twice its width because each width is equal to one alien
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    # To determine the number of rows, we find the available vertical
    # space by subtracting the alien height from the top, the ship height from the
    # bottom, and two alien heights from the bottom of the screen
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    # To find the number of rows, we divide the available
    # space by two times the height of an alien
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    # Create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # Each alien is
    # pushed to the right one alien width from the left margin. Next, we multiply the alien width by 2 to account for the space each alien takes up,
    # including the empty space to its right, and we multiply this amount by
    # the alien’s position in the row. Then we add each new alien to the group
    # aliens.
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """respond appropriately if any aliens have reached an edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change its direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    # multiplying by -1 flips the flag, reversing the fleet's direction
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if any aliens have reached teh bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if the fleet is at an edge, and then update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """respond to a ship being hit by an alien"""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Update images on the screen and flip to the new screen
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # draws the ship at its location
    ship.blitme()

    # Draw aliens
    # When you call draw() on a group, Pygame automatically draws each element in the group at the position defined by its rect attribute. In this case,
    # aliens.draw(screen) draws each alien in the group to the screen.
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible so that it continually updates the display
    pygame.display.flip()
