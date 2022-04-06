import pygame
from pygame.sprite import Group
from game_stats import GameStats

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from slasher import Slasher
import game_functions as gf

def run_game():
    #Initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()    
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Lil Slasher Shoot")

    #Make the Play button
    play_button = Button(ai_settings, screen, "Play")
    
    #Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    #Make a slasher, a group of bullets, and a group of zombies
    slasher = Slasher(ai_settings, screen)
    bullets = Group()
    zombies = Group()

    #Create the horde of zombies
    gf.create_horde(ai_settings, screen, slasher, zombies)
    
    #Start the main loop for the game
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, slasher, zombies, bullets)
        if stats.game_active:
            slasher.update()
            gf.update_bullets(ai_settings, screen, stats, sb, slasher, zombies, bullets)  
            gf.update_zombies(ai_settings, screen, stats, sb, slasher, zombies, bullets)     
        gf.update_screen(ai_settings, screen, stats, sb, slasher, zombies, bullets, play_button)

run_game()