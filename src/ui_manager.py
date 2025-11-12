import pygame
import cv2
import numpy as np
import math
import random

class UIManager:
    def __init__(self, width, height):
        """Initialize UI manager"""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Expressify - Face Expression Game")

        # Colors - More vibrant and fun!
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (50, 255, 130)
        self.RED = (255, 69, 96)
        self.BLUE = (64, 156, 255)
        self.YELLOW = (255, 220, 50)
        self.PURPLE = (155, 89, 182)
        self.ORANGE = (255, 159, 64)
        self.PINK = (255, 105, 180)
        self.CYAN = (64, 224, 208)
        self.GRAY = (128, 128, 128)
        self.DARK_PURPLE = (45, 20, 70)
        self.LIGHT_BLUE = (135, 206, 250)

        # Fonts
        self.title_font = pygame.font.Font(None, 92)
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Animation variables
        self.menu_time = 0
        self.particles = []
        self.init_particles()
        
    def init_particles(self):
        """Initialize floating particles for background"""
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(3, 12),
                'speed': random.uniform(0.5, 2),
                'color': random.choice([self.PURPLE, self.PINK, self.CYAN, 
                                       self.ORANGE, self.YELLOW, self.LIGHT_BLUE]),
                'direction': random.uniform(0, 2 * math.pi)
            })
    
    def draw_gradient_background(self, color1, color2):
        """Draw a vertical gradient background"""
        for y in range(self.height):
            progress = y / self.height
            r = int(color1[0] * (1 - progress) + color2[0] * progress)
            g = int(color1[1] * (1 - progress) + color2[1] * progress)
            b = int(color1[2] * (1 - progress) + color2[2] * progress)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def update_particles(self):
        """Update and draw floating particles"""
        for particle in self.particles:
            # Update position
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0
            
            # Draw particle with glow effect
            for i in range(3, 0, -1):
                alpha_surface = pygame.Surface((particle['size'] * i * 2, particle['size'] * i * 2), pygame.SRCALPHA)
                color_with_alpha = (*particle['color'], 50 // i)
                pygame.draw.circle(alpha_surface, color_with_alpha, 
                                 (particle['size'] * i, particle['size'] * i), 
                                 particle['size'] * i)
                self.screen.blit(alpha_surface, 
                               (int(particle['x']) - particle['size'] * i, 
                                int(particle['y']) - particle['size'] * i))
    
    def draw_text_with_shadow(self, text, font, color, x, y, shadow_offset=4):
        """Draw text with shadow for depth effect"""
        # Shadow
        shadow = font.render(text, True, (20, 20, 40))
        shadow_rect = shadow.get_rect(center=(x + shadow_offset, y + shadow_offset))
        self.screen.blit(shadow, shadow_rect)
        
        # Main text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_menu(self):
        """Draw main menu screen with fun animations"""
        self.menu_time += 0.05
        
        # Animated gradient background
        t = math.sin(self.menu_time * 0.5) * 0.5 + 0.5
        color1 = (int(20 + t * 20), int(10 + t * 30), int(40 + t * 40))
        color2 = (int(60 + t * 30), int(20 + t * 20), int(80 + t * 40))
        self.draw_gradient_background(color1, color2)
        
        # Update and draw particles
        self.update_particles()
        
        # Draw decorative circles
        pulse = math.sin(self.menu_time) * 20
        for i in range(5):
            alpha = int(30 - i * 5)
            size = int(150 + pulse + i * 30)
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*self.PURPLE, alpha), (size, size), size, 3)
            self.screen.blit(circle_surface, (self.width // 2 - size, 150 - size))
        
        # Animated title with bounce effect
        bounce = math.sin(self.menu_time * 2) * 10
        title_y = 150 + bounce
        
        # Draw title with rainbow gradient effect
        title_text = "EXPRESSIFY"
        char_surfaces = []
        total_width = 0
        
        for i, char in enumerate(title_text):
            # Rainbow colors for each character
            hue = (self.menu_time * 50 + i * 30) % 360
            color = self.hsv_to_rgb(hue, 100, 100)
            char_surface = self.title_font.render(char, True, color)
            char_surfaces.append(char_surface)
            total_width += char_surface.get_width()
        
        # Draw each character with slight offset
        x_offset = (self.width - total_width) // 2
        for i, char_surface in enumerate(char_surfaces):
            char_bounce = math.sin(self.menu_time * 2 + i * 0.3) * 8
            shadow = self.title_font.render(title_text[i], True, (20, 20, 40))
            self.screen.blit(shadow, (x_offset + 4, title_y + char_bounce + 4))
            self.screen.blit(char_surface, (x_offset, title_y + char_bounce))
            x_offset += char_surface.get_width()
        
        # Subtitle with glow
        subtitle_y = 240
        self.draw_text_with_glow("Face Expression Game", self.medium_font, 
                                 self.CYAN, self.width // 2, subtitle_y)
        
        # Decorative shapes instead of emoji
        emoji_bounce = math.sin(self.menu_time * 1.5) * 5
        # Draw left star
        self.draw_star(200, subtitle_y + emoji_bounce, 25, self.YELLOW)
        # Draw right star
        self.draw_star(self.width - 200, subtitle_y - emoji_bounce, 25, self.PINK)
        
        # Fancy instruction box
        box_y = 340
        box_height = 220
        box_rect = pygame.Rect(self.width // 2 - 400, box_y, 800, box_height)
        
        # Draw box with border glow
        for i in range(5, 0, -1):
            alpha = 50 - i * 8
            border_surface = pygame.Surface((box_rect.width + i * 4, box_rect.height + i * 4), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (*self.PURPLE, alpha), 
                           border_surface.get_rect(), border_radius=20)
            self.screen.blit(border_surface, 
                           (box_rect.x - i * 2, box_rect.y - i * 2))
        
        # Box background with transparency
        box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (30, 20, 50, 180), box_surface.get_rect(), border_radius=20)
        self.screen.blit(box_surface, box_rect)
        
        # Instructions with decorative bullets
        instructions = [
            "Tunjukkan ekspresi wajah sesuai instruksi!",
            "Kamu punya 20 detik untuk skor tertinggi!",
        ]
        
        y_offset = box_y + 40
        for i, text in enumerate(instructions):
            # Draw decorative bullet point
            bullet_color = self.YELLOW if i == 0 else self.CYAN
            pygame.draw.circle(self.screen, bullet_color, 
                             (box_rect.x + 50, y_offset + 10), 8)
            pygame.draw.circle(self.screen, self.WHITE, 
                             (box_rect.x + 50, y_offset + 10), 4)
            
            text_surface = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(text_surface, (box_rect.x + 80, y_offset))
            y_offset += 50
        
        # Start button with pulse animation
        button_y = box_y + 150
        button_pulse = math.sin(self.menu_time * 3) * 5
        button_size = 15 + button_pulse
        
        self.draw_fancy_button("> Tekan SPASI untuk mulai", 
                              self.width // 2, button_y, 
                              self.GREEN, button_size)
        
        # Exit button
        exit_y = button_y + 50
        self.draw_fancy_button("> Tekan ESC untuk keluar", 
                              self.width // 2, exit_y, 
                              self.RED, 10)
        
        # Team info with stylish background
        team_y = self.height - 100
        team_bg = pygame.Surface((self.width, 100), pygame.SRCALPHA)
        pygame.draw.rect(team_bg, (0, 0, 0, 120), team_bg.get_rect())
        self.screen.blit(team_bg, (0, team_y))
        
        team_title = self.small_font.render("* Tim Pengembang:", True, self.YELLOW)
        team_rect = team_title.get_rect(center=(self.width // 2, team_y + 25))
        self.screen.blit(team_title, team_rect)

        members = "Falih Dzakwan Zuhdi • Hamka Putra Andiyan • Bayu Ega Ferdana"
        text = self.small_font.render(members, True, self.LIGHT_BLUE)
        text_rect = text.get_rect(center=(self.width // 2, team_y + 60))
        self.screen.blit(text, text_rect)
    
    def draw_text_with_glow(self, text, font, color, x, y):
        """Draw text with glow effect"""
        # Glow layers
        for i in range(5, 0, -1):
            glow_surface = font.render(text, True, (*color, 50 // i))
            glow_rect = glow_surface.get_rect(center=(x, y))
            
            alpha_surface = pygame.Surface((glow_rect.width + i * 4, glow_rect.height + i * 4), pygame.SRCALPHA)
            alpha_surface.blit(glow_surface, (i * 2, i * 2))
            self.screen.blit(alpha_surface, (glow_rect.x - i * 2, glow_rect.y - i * 2))
        
        # Main text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_fancy_button(self, text, x, y, color, pulse_size):
        """Draw a fancy button with animation"""
        # Background glow
        for i in range(3):
            alpha_value = 40 - i * 10
            glow_surface = pygame.Surface((400 + i * 20, 50 + i * 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, alpha_value), 
                           glow_surface.get_rect(), border_radius=25)
            self.screen.blit(glow_surface, 
                           (x - (200 + i * 10), y - (25 + i * 5)))
        
        # Button background
        button_surface = pygame.Surface((400, 50), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*color, 100), button_surface.get_rect(), border_radius=25)
        self.screen.blit(button_surface, (x - 200, y - 25))
        
        # Button border
        pygame.draw.rect(self.screen, color, (x - 200, y - 25, 400, 50), 
                        width=3, border_radius=25)
        
        # Text
        text_surface = self.small_font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV color to RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def draw_star(self, x, y, size, color):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            radius = size if i % 2 == 0 else size / 2
            points.append((
                x + math.cos(angle) * radius,
                y + math.sin(angle) * radius
            ))
        
        # Draw glow
        for i in range(3, 0, -1):
            glow_points = []
            for px, py in points:
                glow_points.append((
                    x + (px - x) * (1 + i * 0.2),
                    y + (py - y) * (1 + i * 0.2)
                ))
            alpha_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            pygame.draw.polygon(alpha_surface, (*color, 50 // i), 
                              [(px - x + size * 2, py - y + size * 2) for px, py in glow_points])
            self.screen.blit(alpha_surface, (x - size * 2, y - size * 2))
        
        # Draw star
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, self.WHITE, points, 2)

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

        # DEBUG: Draw expression indicator with text
        expression_labels = {
            'happy': 'SENANG',
            'sad': 'SEDIH', 
            'surprised': 'KAGET',
            'neutral': 'NETRAL'
        }
        label = expression_labels.get(detected_expression, 'TIDAK DIKETAHUI')
        emoji_text = f"Ekspresi: {label}"
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
            message = "*** LUAR BIASA! ***"
            color = self.GREEN
        elif percentage >= 60:
            message = "++ BAGUS SEKALI! ++"
            color = self.BLUE
        elif percentage >= 40:
            message = "= CUKUP BAIK! ="
            color = self.WHITE
        else:
            message = "~ TERUS BERLATIH! ~"
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
