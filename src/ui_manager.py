import pygame
import cv2
import numpy as np


class UIManager:
    def __init__(self, width, height):
        """Initialize UI manager"""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Expressify - Face Expression Game")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 120, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)

    def draw_menu(self):
        """Draw main menu screen"""
        self.screen.fill(self.BLACK)

        # Title
        title = self.title_font.render("EXPRESSIFY", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.medium_font.render("Face Expression Game", True, self.WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)

        # Instructions
        instructions = [
            "Tunjukkan ekspresi wajah sesuai instruksi!",
            "Kamu punya 20 detik untuk skor tertinggi!",
            "",
            "Tekan SPASI untuk mulai",
            "Tekan ESC untuk keluar",
        ]

        y_offset = 320
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40

        # Team info
        team_y = self.height - 120
        team_title = self.small_font.render("Tim Pengembang:", True, self.GRAY)
        team_rect = team_title.get_rect(center=(self.width // 2, team_y))
        self.screen.blit(team_title, team_rect)

        members = ["Falih Dzakwan Zuhdi • Hamka Putra Andiyan • Bayu Ega Ferdana"]
        for i, member in enumerate(members):
            text = self.small_font.render(member, True, self.GRAY)
            text_rect = text.get_rect(center=(self.width // 2, team_y + 35 + (i * 30)))
            self.screen.blit(text, text_rect)

    def draw_game(self, frame, current_challenge, score, remaining_time):
        """Draw game playing screen"""
        self.screen.fill(self.BLACK)

        # Convert OpenCV frame to Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

        # Scale and position camera feed
        camera_width = 640
        camera_height = 480
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        frame_surface = pygame.transform.scale(
            frame_surface, (camera_width, camera_height)
        )
        self.screen.blit(frame_surface, (camera_x, camera_y))

        # Draw challenge text
        from game_logic import GameLogic

        game_logic = GameLogic()
        challenge_text = game_logic.expression_names.get(current_challenge, "")
        challenge = self.large_font.render(challenge_text, True, self.YELLOW)
        challenge_rect = challenge.get_rect(center=(self.width // 2, 50))
        self.screen.blit(challenge, challenge_rect)

        # Draw score
        score_text = f"Skor: {score}"
        score_surface = self.medium_font.render(score_text, True, self.GREEN)
        self.screen.blit(score_surface, (50, 30))

        # Draw timer
        time_text = f"Waktu: {int(remaining_time)}s"
        time_color = self.RED if remaining_time < 5 else self.WHITE
        time_surface = self.medium_font.render(time_text, True, time_color)
        time_rect = time_surface.get_rect(topright=(self.width - 50, 30))
        self.screen.blit(time_surface, time_rect)

    def draw_game_with_debug(self, frame, current_challenge, score, remaining_time, detected_expression):
        """Draw game playing screen with debug info"""
        self.screen.fill(self.BLACK)

        # Convert OpenCV frame to Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

        # Scale and position camera feed
        camera_width = 640
        camera_height = 480
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        frame_surface = pygame.transform.scale(
            frame_surface, (camera_width, camera_height)
        )
        self.screen.blit(frame_surface, (camera_x, camera_y))

        # Draw challenge text
        from game_logic import GameLogic

        game_logic = GameLogic()
        challenge_text = game_logic.expression_names.get(current_challenge, "")
        challenge = self.large_font.render(challenge_text, True, self.YELLOW)
        challenge_rect = challenge.get_rect(center=(self.width // 2, 50))
        self.screen.blit(challenge, challenge_rect)

        # Draw score
        score_text = f"Skor: {score}"
        score_surface = self.medium_font.render(score_text, True, self.GREEN)
        self.screen.blit(score_surface, (50, 30))

        # Draw timer
        time_text = f"Waktu: {int(remaining_time)}s"
        time_color = self.RED if remaining_time < 5 else self.WHITE
        time_surface = self.medium_font.render(time_text, True, time_color)
        time_rect = time_surface.get_rect(topright=(self.width - 50, 30))
        self.screen.blit(time_surface, time_rect)

        # DEBUG: Draw detected expression
        detected_text = f"Terdeteksi: {detected_expression}"
        detected_color = self.GREEN if detected_expression == current_challenge else self.RED
        detected_surface = self.medium_font.render(detected_text, True, detected_color)
        self.screen.blit(detected_surface, (50, 70))

        # DEBUG: Draw emoji based on detected
        emoji_map = {
            'happy': '😊',
            'sad': '😢', 
            'surprised': '😲',
            'neutral': '😐'
        }
        emoji = emoji_map.get(detected_expression, '❓')
        emoji_text = f"Ekspresi: {emoji}"
        emoji_surface = self.large_font.render(emoji_text, True, self.WHITE)
        emoji_rect = emoji_surface.get_rect(topright=(self.width - 50, 70))
        self.screen.blit(emoji_surface, emoji_rect)

    def draw_results(self, score, max_score):
        """Draw results screen"""
        self.screen.fill(self.BLACK)

        # Title
        title = self.title_font.render("GAME OVER!", True, self.RED)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)

        # Score
        score_text = f"Skor Akhir: {score}"
        score_surface = self.large_font.render(score_text, True, self.YELLOW)
        score_rect = score_surface.get_rect(center=(self.width // 2, 280))
        self.screen.blit(score_surface, score_rect)

        # Performance message
        percentage = (score / max_score * 100) if max_score > 0 else 0
        if percentage >= 80:
            message = "🌟 LUAR BIASA! 🌟"
            color = self.GREEN
        elif percentage >= 60:
            message = "👍 BAGUS SEKALI! 👍"
            color = self.BLUE
        elif percentage >= 40:
            message = "😊 CUKUP BAIK! 😊"
            color = self.WHITE
        else:
            message = "💪 TERUS BERLATIH! 💪"
            color = self.GRAY

        message_surface = self.medium_font.render(message, True, color)
        message_rect = message_surface.get_rect(center=(self.width // 2, 370))
        self.screen.blit(message_surface, message_rect)

        # Restart instruction
        restart_text = "Tekan SPASI untuk main lagi"
        restart_surface = self.small_font.render(restart_text, True, self.WHITE)
        restart_rect = restart_surface.get_rect(center=(self.width // 2, 480))
        self.screen.blit(restart_surface, restart_rect)

        exit_text = "Tekan ESC untuk keluar"
        exit_surface = self.small_font.render(exit_text, True, self.GRAY)
        exit_rect = exit_surface.get_rect(center=(self.width // 2, 520))
        self.screen.blit(exit_surface, exit_rect)
