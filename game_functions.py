import sys
import pygame
from bullet import Bullet
from zombie import Zombie
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        slasher.moving_right = True
    elif event.key == pygame.K_LEFT:
        slasher.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, slasher, bullets)
    elif event.key == pygame.K_p:
        play_button.game_start = True
        game_start(ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, slasher):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        slasher.moving_right = False
    elif event.key == pygame.K_LEFT:
        slasher.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked:
                play_button.game_start = True
                game_start(ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, slasher)

def update_screen(ai_settings, screen, stats, sb, slasher, zombies, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    #Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind slasher and zombies
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    slasher.blitme()
    zombies.draw(screen)

    #Draw the score information
    sb.show_score()
    
    #Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    #Make the most recently drawn screen visible
    pygame.display.flip()

def game_start(ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets):
    """Start a new game when the player clicks Play"""
    if play_button.game_start and not stats.game_active:
        #Reset the game settings
        ai_settings.initialize_dynamic_settings()
        
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        #Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_slashers()
        
        #Empty the list of zombies and bullets
        zombies.empty()
        bullets.empty()

        #Create a new horde and center the slasher
        create_horde(ai_settings, screen, slasher, zombies)
        slasher.center_slasher()

def get_number_zombies_x(ai_settings, zombie_width):
    """Determine the number of zombies that fit in a row"""
    available_space_x = ai_settings.screen_width -2 * zombie_width
    number_zombies_x = int(available_space_x / (2 * zombie_width))
    return number_zombies_x

def get_number_rows(ai_settings, slasher_height, zombie_height):
    """Determine the number of rows of zombies that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * zombie_height) - slasher_height)
    number_rows = int(available_space_y / (2 * zombie_height))
    return number_rows

def create_zombie(ai_settings, screen, zombies, zombie_number, row_number):
    """Create an zombie and place it in the row"""
    zombie = Zombie(ai_settings, screen)
    zombie_width = zombie.rect.width
    zombie.x = zombie_width + 2 * zombie_width * zombie_number
    zombie.rect.x = zombie.x
    zombie.rect.y = zombie.rect.height + 2 * zombie.rect.height * row_number
    zombies.add(zombie)

def create_horde(ai_settings, screen, slasher, zombies):
    """Create a full horde of zombies"""
    #Create an zombie and find the number of zombies in a row
    zombie = Zombie(ai_settings, screen)
    number_zombies_x = get_number_zombies_x(ai_settings, zombie.rect.width)
    number_rows = get_number_rows(ai_settings, slasher.rect.height, zombie.rect.height)

    #Create the horde of zombies
    for row_number in range(number_rows):
        for zombie_number in range(number_zombies_x):
            create_zombie(ai_settings, screen, zombies, zombie_number, row_number)

def check_horde_edges(ai_settings, zombies):
    """Respond appropriately if any zombies have reached an edge"""
    for zombie in zombies.sprites():
        if zombie.check_edges():
            change_horde_direction(ai_settings, zombies)
            break

def change_horde_direction(ai_settings, zombies):
    """Drop the entire horde and change the horde's direction"""
    for zombie in zombies.sprites():
        zombie.rect.y += ai_settings.horde_drop_speed
    ai_settings.horde_direction *= -1

def update_zombies(ai_settings, screen, stats, sb, slasher, zombies, bullets):
    """Check if the horde is at an edge, and then update the position of all zombies in the horde"""
    check_horde_edges(ai_settings, zombies)
    zombies.update()

    #Look for zombie-slasher collisions
    if pygame.sprite.spritecollideany(slasher, zombies):
        slasher_hit(ai_settings, screen, stats, sb, slasher, zombies, bullets)
    
    #Look for zombies hitting the bottom of the screen
    check_zombies_bottom(ai_settings, screen, stats, sb, slasher, zombies, bullets)

def check_zombies_bottom(ai_settings, screen, stats, sb, slasher, zombies, bullets):
    """Check if any zombies have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for zombie in zombies.sprites():
        if zombie.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the slasher got hit
            slasher_hit(ai_settings, screen, stats, sb, slasher, zombies, bullets)
            break

def fire_bullet(ai_settings, screen, slasher, bullets):
    """Fire a bullet if limit not reached yet"""
    #Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, slasher)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, slasher, zombies, bullets):
    """Update position of bullets and get rid of old bullets"""
    bullets.update()
    #Get rid of bullets that have dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_zombie_collisions(ai_settings, screen, stats, sb, slasher, zombies, bullets)

def check_bullet_zombie_collisions(ai_settings, screen, stats, sb, slasher, zombies, bullets):
    """Respond to bullet-zombie collisions"""
    #Remove any bullets and zombies that have collided
    collisions = pygame.sprite.groupcollide(bullets, zombies, True, True)
    if collisions:
        for zombies in collisions.values():
            stats.score += ai_settings.zombie_points * len(zombies)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(zombies) == 0:
        #If the entire horde is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        #ncrease level
        stats.level += 1
        sb.prep_level()

        create_horde(ai_settings, screen, slasher, zombies)
    
def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def slasher_hit(ai_settings, screen, stats, sb, slasher, zombies, bullets):
    """Respond to slasher being hit by zombie"""
    if stats.slashers_left > 0:
        #Decrement slashers_left
        stats.slashers_left -= 1

        #Update scoreboard
        sb.prep_slashers()
        
        #Empty the list of zombies and bullets
        zombies.empty()
        bullets.empty()

        #Create a new horde and center the slasher
        create_horde(ai_settings, screen, slasher, zombies)
        slasher.center_slasher()

        #Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)