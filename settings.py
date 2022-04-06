class Settings():
    """A class to store all settings for zombie Invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        #slasher settings
        self.slasher_speed_factor = 1.5
        self.slasher_limit = 3

        #Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 230, 0, 0
        self.bullets_allowed = 3

        #zombie settings
        self.zombie_speed_factor = 1
        self.horde_drop_speed = 10
        self.horde_direction = 1

        #How quickly the game speeds up
        self.speedup_scale = 1.1
        #How quickly the zombie point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.slasher_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.zombie_speed_factor = 1

        #gleet_direction of 1 represents right; -1 represents left
        self.horde_direction = 1

        #Scoring
        self.zombie_points = 50

    def increase_speed(self):
        """Increase speed settings and zombie point values"""
        self.slasher_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.zombie_speed_factor *= self.speedup_scale

        self.zombie_points = int(self.zombie_points * self.score_scale)