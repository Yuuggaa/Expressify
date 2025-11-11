import cv2
import pygame
from face_detector import FaceDetector
from game_logic import GameLogic
from ui_manager import UIManager

class Expressify:
    def __init__(self):
        """Initialize game components"""
        pygame.init()

        # Game settings
        self.GAME_DURATION = 20  # seconds
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        # Initialize components
        self.face_detector = FaceDetector()
        self.game_logic = GameLogic(self.GAME_DURATION)
        self.ui_manager = UIManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Game states
        self.running = True
        self.game_state = "menu"  # menu, playing, results

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)

            # Update game based on state
            if self.game_state == "menu":
                self.ui_manager.draw_menu()
            elif self.game_state == "playing":
                self.play_game()
            elif self.game_state == "results":
                self.ui_manager.draw_results(
                    self.game_logic.score, self.game_logic.max_score
                )

            pygame.display.flip()
            clock.tick(30)

        self.cleanup()

    def play_game(self):
        """Game playing logic"""
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)

        # Detect face and expression
        expression_detected = self.face_detector.detect_expression(frame)

        # Update game logic
        self.game_logic.update(expression_detected)

        # Draw UI with debug info
        self.ui_manager.draw_game_with_debug(
            frame,
            self.game_logic.current_expression,
            self.game_logic.score,
            self.game_logic.get_remaining_time(),
            expression_detected
        )

        # Check if game is over
        if self.game_logic.is_game_over():
            self.game_state = "results"

    def handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_SPACE:
            if self.game_state == "menu":
                self.game_state = "playing"
                self.game_logic.start_game()
            elif self.game_state == "results":
                self.game_state = "menu"
                self.game_logic.reset()
        elif key == pygame.K_ESCAPE:
            self.running = False

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    game = Expressify()
    game.run()
