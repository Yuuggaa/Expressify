import cv2
import pygame
import sys
import os
from face_detector import FaceDetector
from game_logic import GameLogic
from ui import UIManager
from sound_manager import SoundManager
from leaderboard_manager import LeaderboardManager


# Get base path for assets (works with PyInstaller)
def get_base_path():
    """Get base path for assets, works in dev and frozen (exe) mode"""
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running in development
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Set base path globally
BASE_PATH = get_base_path()

# 💡 Inisialisasi mixer sebelum pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


class Expressify:
    def __init__(self):
        """Initialize game components"""

        # Game settings
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.is_fullscreen = False

        # Create window (windowed mode by default)
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Expressify - Face Expression Game")

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
        self.leaderboard_difficulty_index = 1  # 0=easy, 1=medium, 2=hard

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        menu_bgm_played = False  # 🔹 flag untuk menu BGM

        while self.running:
            # Reset cursor to default at start of each frame
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_mouse_click(event.pos)
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    if not self.is_fullscreen:
                        self.WINDOW_WIDTH = event.w
                        self.WINDOW_HEIGHT = event.h
                        self.screen = pygame.display.set_mode(
                            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE
                        )
                        self.ui_manager = UIManager(
                            self.WINDOW_WIDTH, self.WINDOW_HEIGHT
                        )

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
            self.sound_manager.stop("bgm")

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
        # Toggle fullscreen with F11
        if key == pygame.K_F11:
            self.toggle_fullscreen()
            return

        if self.game_state == "menu":
            if key == pygame.K_LEFT:
                self.menu_index = max(0, self.menu_index - 1)
            elif key == pygame.K_RIGHT:
                self.menu_index = min(2, self.menu_index + 1)
            elif key == pygame.K_RETURN:
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
            elif key == pygame.K_RETURN:
                self.sound_manager.play("start")
                # Set difficulty and start game
                difficulties = ["easy", "medium", "hard"]
                self.difficulty = difficulties[self.difficulty_index]
                self.game_logic = GameLogic(difficulty=self.difficulty)
                # Stop menu BGM before starting game
                self.sound_manager.stop("bgm")
                self.sound_manager.play("bgm", loops=-1)
                self.game_state = "playing"
                self.game_logic.start_game()
            elif key == pygame.K_ESCAPE:
                self.game_state = "name_input"

        elif self.game_state == "leaderboard":
            if key == pygame.K_LEFT:
                self.leaderboard_difficulty_index = max(
                    0, self.leaderboard_difficulty_index - 1
                )
                difficulties = ["easy", "medium", "hard"]
                self.leaderboard_difficulty = difficulties[
                    self.leaderboard_difficulty_index
                ]
                self.sound_manager.play("click")
            elif key == pygame.K_RIGHT:
                self.leaderboard_difficulty_index = min(
                    2, self.leaderboard_difficulty_index + 1
                )
                difficulties = ["easy", "medium", "hard"]
                self.leaderboard_difficulty = difficulties[
                    self.leaderboard_difficulty_index
                ]
                self.sound_manager.play("click")
            elif key == pygame.K_ESCAPE:
                self.game_state = "menu"

        elif self.game_state == "results":
            if key == pygame.K_RETURN:
                self.sound_manager.play("start")
                self.game_state = "difficulty_select"
                self.sound_manager.stop("high_score")
                self.sound_manager.stop("botHigh_score")
                self.sound_manager.stop("upLow_score")
                self.sound_manager.stop("low_score")
                self.sound_manager.play("bgm", loops=-1)
                self.game_logic.reset()
            elif key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.menu_index = 0
                self.player_name = ""  # Reset nama ketika kembali ke menu

    def handle_mouse_click(self, pos):
        """Handle mouse click events"""
        if self.game_state == "menu":
            # Get button rectangles from menu screen
            button_rects = self.ui_manager.menu_screen.get_button_rects()
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(pos):
                    self.menu_index = i
                    self.sound_manager.play("start")
                    if self.menu_index == 0:  # Play
                        self.game_state = "name_input"
                        self.player_name = ""
                    elif self.menu_index == 1:  # Leaderboard
                        self.game_state = "leaderboard"
                    elif self.menu_index == 2:  # Quit
                        self.running = False
                    break

        elif self.game_state == "difficulty_select":
            # Get difficulty button rectangles
            button_rects = self.ui_manager.difficulty_screen.get_button_rects()
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(pos):
                    self.difficulty_index = i
                    self.sound_manager.play("start")
                    difficulties = ["easy", "medium", "hard"]
                    self.difficulty = difficulties[self.difficulty_index]
                    self.game_logic = GameLogic(difficulty=self.difficulty)
                    self.sound_manager.stop("bgm")
                    self.sound_manager.play("bgm", loops=-1)
                    self.game_state = "playing"
                    self.game_logic.start_game()
                    break

        elif self.game_state == "leaderboard":
            # Check if clicked on difficulty tabs
            tab_rects = self.ui_manager.leaderboard_screen.get_tab_rects()
            for i, rect in enumerate(tab_rects):
                if rect.collidepoint(pos):
                    difficulties = ["easy", "medium", "hard"]
                    self.leaderboard_difficulty_index = i
                    self.leaderboard_difficulty = difficulties[i]
                    self.sound_manager.play("click")
                    break

            # Check back button
            back_rect = self.ui_manager.leaderboard_screen.get_back_button_rect()
            if back_rect and back_rect.collidepoint(pos):
                self.game_state = "menu"
                self.sound_manager.play("click")

        elif self.game_state == "results":
            # Get play again and menu button rectangles
            button_rects = self.ui_manager.results_screen.get_button_rects()
            if len(button_rects) >= 2:
                # Play Again button
                if button_rects[0].collidepoint(pos):
                    self.sound_manager.play("start")
                    self.game_state = "difficulty_select"
                    self.sound_manager.stop("high_score")
                    self.sound_manager.stop("botHigh_score")
                    self.sound_manager.stop("upLow_score")
                    self.sound_manager.stop("low_score")
                    self.sound_manager.play("bgm", loops=-1)
                    self.game_logic.reset()
                # Main Menu button
                elif button_rects[1].collidepoint(pos):
                    self.game_state = "menu"
                    self.menu_index = 0
                    self.player_name = ""
                    self.sound_manager.play("click")

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Get actual fullscreen resolution
            info = pygame.display.Info()
            self.WINDOW_WIDTH = info.current_w
            self.WINDOW_HEIGHT = info.current_h
        else:
            # Switch back to windowed mode
            self.WINDOW_WIDTH = 1280
            self.WINDOW_HEIGHT = 720
            self.screen = pygame.display.set_mode(
                (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE
            )

        # Recreate UI manager with new dimensions
        self.ui_manager = UIManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        print(
            f"{'Fullscreen' if self.is_fullscreen else 'Windowed'} mode: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        )

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    game = Expressify()
    game.run()
