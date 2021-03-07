class Gamestats:
    """track statistics for alien invasion"""

    def __init__(self, ai_settings):
        """initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # start game in inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        """To reset the score each time a new game starts, we initialize score in reset_stats() rather than __init__()."""
        self.score = 0
        self.level = 1
