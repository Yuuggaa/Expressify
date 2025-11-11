import cv2
import pygame
from face_detector import FaceDetector
from game_logic import GameLogic
from ui_manager import UIManager
from sound_manager import SoundManager

# 💡 Inisialisasi mixer sebelum pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

class Expressify:
    def __init__(self):
        """Initialize game components"""

        # Game settings
        self.GAME_DURATION = 20  # seconds
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        # Initialize components
        self.face_detector = FaceDetector()
        self.game_logic = GameLogic(self.GAME_DURATION)
        self.ui_manager = UIManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.sound_manager = SoundManager() 

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Game states
        self.running = True
        self.game_state = "menu"  # menu, playing, results

        # ✅ Play BGM hanya sekali di awal
        

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        bgm_played = False  # 🔹 flag agar BGM hanya sekali diputar

        while self.running:
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
                # 🔹 mainkan BGM hanya sekali
                if not bgm_played:
                    self.sound_manager.play("bgm")
                    bgm_played = True

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
        
        frame = cv2.flip(frame, 1)
        expression_detected = self.face_detector.detect_expression(frame)
        self.game_logic.update(expression_detected)

        self.ui_manager.draw_game_with_debug(
            frame,
            self.game_logic.current_expression,
            self.game_logic.score,
            self.game_logic.get_remaining_time(),
            expression_detected
        )

        if self.game_logic.is_game_over():
            self.game_state = "results"
            self.sound_manager.stop("bgm")  # ✅ stop bgm saat game selesai
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
        if key == pygame.K_SPACE:
            if self.game_state == "menu":
                self.game_state = "playing"
                self.sound_manager.play("start")
                self.game_logic.start_game()
            elif self.game_state == "results":
                self.game_state = "menu"
                self.sound_manager.stop("high_score")
                self.sound_manager.stop("botHigh_score")
                self.sound_manager.stop("upLow_score")
                self.sound_manager.stop("low_score")
                self.sound_manager.play("bgm")  # ✅ putar ulang bgm saat restart
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
