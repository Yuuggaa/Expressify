"""
Game Logic Module
Handles game state, scoring, and expression challenges
"""

import random
import time


class GameLogic:
    def __init__(self, game_duration=20):
        """Initialize game logic"""
        self.game_duration = game_duration
        self.score = 0
        self.max_score = 0
        self.current_expression = None
        self.start_time = None
        self.last_expression_time = None
        self.expression_duration = 3  # seconds per expression

        # Available expressions for challenges
        self.expressions = ["happy", "sad", "surprised", "neutral"]

        # Expression names in Indonesian
        self.expression_names = {
            "happy": "😊 SENYUM LEBAR!",
            "sad": "😢 CEMBERUT SEDIH!",
            "surprised": "😲 KAGET MAKSIMAL!",
            "neutral": "😐 WAJAH DATAR!",
        }

    def start_game(self):
        """Start a new game"""
        self.score = 0
        self.start_time = time.time()
        self.last_expression_time = time.time()
        # TESTING MODE: Set to happy only for calibration
        self.current_expression = "happy"  # random.choice(self.expressions)
        self.max_score = int(self.game_duration / self.expression_duration)

    def update(self, detected_expression):
        """
        Update game state based on detected expression
        Returns: True if score increased
        """
        if not self.start_time:
            return False

        current_time = time.time()

        # Check if current challenge matches detected expression
        if detected_expression == self.current_expression:
            # Check if enough time has passed since last score
            if current_time - self.last_expression_time >= 1.0:  # 1 second cooldown
                self.score += 1
                self.last_expression_time = current_time
                # Generate new challenge
                self.current_expression = random.choice(self.expressions)
                return True

        return False

    def get_remaining_time(self):
        """Get remaining game time in seconds"""
        if not self.start_time:
            return self.game_duration

        elapsed = time.time() - self.start_time
        remaining = max(0, self.game_duration - elapsed)
        return remaining

    def is_game_over(self):
        """Check if game time is up"""
        return self.get_remaining_time() <= 0

    def get_current_challenge(self):
        """Get current expression challenge text"""
        if self.current_expression:
            return self.expression_names.get(self.current_expression, "UNKNOWN")
        return ""

    def reset(self):
        """Reset game to initial state"""
        self.score = 0
        self.max_score = 0
        self.current_expression = None
        self.start_time = None
        self.last_expression_time = None
