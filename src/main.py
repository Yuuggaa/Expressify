import cv2
import pygame
from face_detector import FaceDetector
from game_logic import GameLogic
from ui_manager import UIManager
from sound_manager import SoundManager
from leaderboard_manager import LeaderboardManager

# 💡 Inisialisasi mixer sebelum pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


class Expressify:
    def __init__(self):
        """Initialize game components"""

        # Game settings
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        # Initialize components
        self.face_detector = FaceDetector()
        self.ui_manager = UIManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.sound_manager = SoundManager()
        self.leaderboard = LeaderboardManager()

        # Difficulty settings
        self.difficulty = "medium"
        self.difficulty_index = 1  # 0=easy, 1=medium, 2=hard
        self.game_logic = GameLogic(difficulty=self.difficulty)

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Game states
        self.running = True
        self.game_state = (
            "menu"  # menu, name_input, difficulty_select, playing, results, leaderboard
        )

        # Menu navigation
        self.menu_index = 0  # 0=play, 1=leaderboard, 2=quit

        # Player info
        self.player_name = ""

        # Leaderboard view
        self.leaderboard_difficulty = "medium"

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        menu_bgm_played = False  # 🔹 flag untuk menu BGM

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)

            # Update game based on state
            if self.game_state == "menu":
                # Play menu BGM with infinite loop
                if not menu_bgm_played:
                    self.sound_manager.play("bgm", loops=-1)
                    menu_bgm_played = True
                self.ui_manager.draw_menu(self.menu_index)
            elif self.game_state == "name_input":
                self.ui_manager.draw_name_input(self.player_name)
            elif self.game_state == "difficulty_select":
                self.ui_manager.draw_difficulty_selection(self.difficulty_index)
            elif self.game_state == "playing":
                self.play_game()
            elif self.game_state == "results":
                self.ui_manager.draw_results(
                    self.game_logic.score, self.game_logic.max_score
                )
            elif self.game_state == "leaderboard":
                self.ui_manager.draw_leaderboard(
                    self.leaderboard, self.leaderboard_difficulty
                )

            pygame.display.flip()
            clock.tick(30)

        self.cleanup()

    def play_game(self):
        """Game playing logic"""
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        expression_detected = self.face_detector.detect_expression(frame)
        self.game_logic.update(expression_detected)

        self.ui_manager.draw_game_with_debug(
            frame,
            self.game_logic.current_expression,
            self.game_logic.score,
            self.game_logic.get_remaining_time(),
            expression_detected,
        )

        if self.game_logic.is_game_over():
            self.game_state = "results"
            self.sound_manager.stop("bgm")  # ✅ stop bgm saat game selesai

            # Save score to leaderboard with player name
            player_name = self.player_name if self.player_name else "Player"
            rank = self.leaderboard.add_score(
                self.difficulty, self.game_logic.score, player_name
            )
            print(f"Score saved! Player: {player_name}, Rank: {rank}")

            # Play sound based on score
            if self.game_logic.score >= (0.8 * self.game_logic.max_score):
                self.sound_manager.play("high_score")
            elif self.game_logic.score >= (0.6 * self.game_logic.max_score):
                self.sound_manager.play("botHigh_score")
            elif self.game_logic.score >= (0.4 * self.game_logic.max_score):
                self.sound_manager.play("upLow_score")
            else:
                self.sound_manager.play("low_score")

    def handle_keypress(self, key):
        """Handle keyboard input"""
        if self.game_state == "menu":
            if key == pygame.K_LEFT:
                self.menu_index = max(0, self.menu_index - 1)
            elif key == pygame.K_RIGHT:
                self.menu_index = min(2, self.menu_index + 1)
            elif key == pygame.K_SPACE:
                self.sound_manager.play("start")
                if self.menu_index == 0:  # Play
                    self.game_state = "name_input"
                    self.player_name = ""
                elif self.menu_index == 1:  # Leaderboard
                    self.game_state = "leaderboard"
                elif self.menu_index == 2:  # Quit
                    self.running = False
            elif key == pygame.K_ESCAPE:
                self.running = False

        elif self.game_state == "name_input":
            if key == pygame.K_RETURN:
                self.sound_manager.play("start")
                # Go to difficulty selection
                if not self.player_name:
                    self.player_name = "Player"
                self.game_state = "difficulty_select"
            elif key == pygame.K_ESCAPE:
                # Skip name input
                self.player_name = "Player"
                self.game_state = "difficulty_select"
            elif key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Add character if valid (A-Z, 0-9, space) and not too long
                if len(self.player_name) < 15:
                    char = pygame.key.name(key)
                    if len(char) == 1:  # Single character
                        if char.isalnum() or char == " ":
                            self.player_name += char.upper()

        elif self.game_state == "difficulty_select":
            if key == pygame.K_UP:
                self.difficulty_index = max(0, self.difficulty_index - 1)
            elif key == pygame.K_DOWN:
                self.difficulty_index = min(2, self.difficulty_index + 1)
            elif key == pygame.K_SPACE:
                self.sound_manager.play("start")
                # Set difficulty and start game
                difficulties = ["easy", "medium", "hard"]
                self.difficulty = difficulties[self.difficulty_index]
                self.game_logic = GameLogic(difficulty=self.difficulty)
                # Stop menu BGM before starting game
                self.sound_manager.stop("bgm")
                self.game_state = "playing"
                self.game_logic.start_game()
            elif key == pygame.K_ESCAPE:
                self.game_state = "name_input"

        elif self.game_state == "leaderboard":
            if key == pygame.K_1:
                self.leaderboard_difficulty = "easy"
            elif key == pygame.K_2:
                self.leaderboard_difficulty = "medium"
            elif key == pygame.K_3:
                self.leaderboard_difficulty = "hard"
            elif key == pygame.K_ESCAPE:
                self.game_state = "menu"

        elif self.game_state == "results":
            if key == pygame.K_SPACE:
                self.sound_manager.play("start")
                self.game_state = "menu"
                self.sound_manager.stop("high_score")
                self.sound_manager.stop("botHigh_score")
                self.sound_manager.stop("upLow_score")
                self.sound_manager.stop("low_score")
                self.sound_manager.play("bgm", loops=-1)
                self.game_logic.reset()
                self.menu_index = 0
            elif key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.menu_index = 0

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    game = Expressify()
    game.run()
