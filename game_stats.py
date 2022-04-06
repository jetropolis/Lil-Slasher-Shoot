class GameStats():
    """Track statistics for Lil Slasher Shoot"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start Lil Slasher Shoot in an inactive state
        self.game_active = False
        #High score should never be reset
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.slashers_left = self.ai_settings.slasher_limit
        self.score = 0