import pygame
import cv2
import numpy as np
import math
import random
import os

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

        # Fonts - Try to load system fonts that support emoji
        try:
            # Try Segoe UI Emoji (Windows emoji font)
            self.emoji_font = pygame.font.SysFont('segoeuiemoji', 72)
            self.symbol_font = pygame.font.SysFont('segoeuiemoji', 28)
        except:
            try:
                # Fallback to Segoe UI Symbol
                self.emoji_font = pygame.font.SysFont('seguisym', 72)
                self.symbol_font = pygame.font.SysFont('seguisym', 28)
            except:
                # Last resort fallback
                self.emoji_font = pygame.font.Font(None, 72)
                self.symbol_font = pygame.font.Font(None, 28)
        
        self.title_font = pygame.font.Font(None, 92)
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Load icon images
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(os.path.dirname(current_dir), "assets", "images")
        
        try:
            self.icon_exchange = pygame.image.load(os.path.join(images_dir, "exchange.png"))
            self.icon_exchange = pygame.transform.scale(self.icon_exchange, (20, 20))
        except:
            self.icon_exchange = None
            
        try:
            self.icon_up_down = pygame.image.load(os.path.join(images_dir, "up-down.png"))
            self.icon_up_down = pygame.transform.scale(self.icon_up_down, (20, 20))
        except:
            self.icon_up_down = None
        
        # Animation variables
        self.menu_time = 0
        self.particles = []
        self.init_particles()
        
        # Expression image settings
        self.animation_time = 0
        self.image_scale = 200  # Ukuran foto dalam pixel
        
        # Load expression photos
        self.expression_images = {}
        self.load_expression_images()
        
        # Floating images for game screen
        self.floating_images = []
        self.init_floating_images()
        
    def load_expression_images(self):
        """Load expression images from assets folder"""
        # Mapping dari ekspresi game ke nama file foto
        image_mapping = {
            "happy": "Senang.png",
            "sad": "Sedih.png", 
            "surprised": "Kaget.png",
            "neutral": "Datar.png"
        }
        
        # Get path to assets folder
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "photo")
        
        for expression, filename in image_mapping.items():
            image_path = os.path.join(base_path, filename)
            try:
                # Load and scale image
                image = pygame.image.load(image_path)
                # Scale to standard size
                image = pygame.transform.scale(image, (self.image_scale, self.image_scale))
                self.expression_images[expression] = image
                print(f"✓ Loaded {expression} image: {filename}")
            except Exception as e:
                print(f"✗ Failed to load {expression} image: {e}")
                # Create placeholder if image fails to load
                placeholder = pygame.Surface((self.image_scale, self.image_scale))
                placeholder.fill(self.PURPLE)
                self.expression_images[expression] = placeholder
    
    def init_floating_images(self):
        """Initialize floating expression images for game background"""
        expressions = ["happy", "sad", "surprised", "neutral"]
        for _ in range(8):  # 8 floating images
            expression = random.choice(expressions)
            self.floating_images.append({
                'expression': expression,
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(40, 80),  # Small size
                'speed': random.uniform(0.3, 0.8),
                'direction': random.uniform(0, 2 * math.pi),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-2, 2),
                'alpha': random.randint(30, 80),  # Semi-transparent
                'bob_offset': random.uniform(0, 2 * math.pi)  # For bobbing animation
            })
    
    def update_floating_images(self):
        """Update and draw floating expression images"""
        for img in self.floating_images:
            # Update position
            img['x'] += math.cos(img['direction']) * img['speed']
            img['y'] += math.sin(img['direction']) * img['speed']
            
            # Wrap around screen
            if img['x'] < -100:
                img['x'] = self.width + 100
            elif img['x'] > self.width + 100:
                img['x'] = -100
            if img['y'] < -100:
                img['y'] = self.height + 100
            elif img['y'] > self.height + 100:
                img['y'] = -100
            
            # Update rotation
            img['rotation'] += img['rotation_speed']
            
            # Get expression image
            if img['expression'] in self.expression_images:
                original_image = self.expression_images[img['expression']]
                
                # Scale down the image
                small_image = pygame.transform.scale(original_image, (img['size'], img['size']))
                
                # Apply rotation
                rotated_image = pygame.transform.rotate(small_image, img['rotation'])
                
                # Create surface with alpha for transparency
                alpha_surface = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
                alpha_surface.blit(rotated_image, (0, 0))
                alpha_surface.set_alpha(img['alpha'])
                
                # Add bobbing motion
                bob = math.sin(self.animation_time * 0.5 + img['bob_offset']) * 8
                
                # Draw the floating image
                final_x = int(img['x'] - rotated_image.get_width() // 2)
                final_y = int(img['y'] + bob - rotated_image.get_height() // 2)
                self.screen.blit(alpha_surface, (final_x, final_y))
    
    def draw_animated_expression_image(self, expression, x, y):
        """Draw expression image with swaying animation"""
        if expression not in self.expression_images:
            return
        
        # Update animation time
        self.animation_time += 0.1
        
        # Calculate swaying motion (left-right)
        sway_amount = 30  # Maximum pixels to sway
        sway_offset = math.sin(self.animation_time) * sway_amount
        
        # Calculate bobbing motion (up-down) - subtle
        bob_amount = 10
        bob_offset = math.sin(self.animation_time * 1.5) * bob_amount
        
        # Calculate rotation - slight tilt
        rotation_amount = 5  # degrees
        rotation = math.sin(self.animation_time * 0.8) * rotation_amount
        
        # Get image and apply rotation
        image = self.expression_images[expression]
        rotated_image = pygame.transform.rotate(image, rotation)
        
        # Calculate final position with animations
        final_x = x + sway_offset - rotated_image.get_width() // 2
        final_y = y + bob_offset - rotated_image.get_height() // 2
        
        # Add glow effect around image
        glow_surface = pygame.Surface(
            (rotated_image.get_width() + 40, rotated_image.get_height() + 40),
            pygame.SRCALPHA
        )
        
        # Multiple glow layers
        for i in range(5, 0, -1):
            alpha = 30 - i * 5
            glow_size = (rotated_image.get_width() + i * 8, rotated_image.get_height() + i * 8)
            temp_surface = pygame.Surface(glow_size, pygame.SRCALPHA)
            
            # Color based on expression
            if expression == "happy":
                glow_color = (*self.YELLOW, alpha)
            elif expression == "sad":
                glow_color = (*self.BLUE, alpha)
            elif expression == "surprised":
                glow_color = (*self.ORANGE, alpha)
            else:  # neutral
                glow_color = (*self.GRAY, alpha)
            
            pygame.draw.rect(temp_surface, glow_color, temp_surface.get_rect(), border_radius=20)
            glow_surface.blit(temp_surface, (20 - i * 4, 20 - i * 4))
        
        # Draw glow
        self.screen.blit(glow_surface, (final_x - 20, final_y - 20))
        
        # Draw the image
        self.screen.blit(rotated_image, (final_x, final_y))
        
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

    def draw_menu(self, selected_index=0):
        """Draw main menu screen with options"""
        self.menu_time += 0.05
        
        # Animated gradient background
        t = math.sin(self.menu_time * 0.5) * 0.5 + 0.5
        color1 = (int(20 + t * 20), int(10 + t * 30), int(40 + t * 40))
        color2 = (int(60 + t * 30), int(20 + t * 20), int(80 + t * 40))
        self.draw_gradient_background(color1, color2)
        
        # Update and draw particles
        self.update_particles()
        
        # Draw floating expression images in background
        self.update_floating_images()
        
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
        ]
        
        y_offset = box_y + 20
        for i, text in enumerate(instructions):
            # Draw decorative bullet point
            bullet_color = self.YELLOW
            pygame.draw.circle(self.screen, bullet_color, 
                             (box_rect.x + 50, y_offset + 10), 8)
            pygame.draw.circle(self.screen, self.WHITE, 
                             (box_rect.x + 50, y_offset + 10), 4)
            
            text_surface = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(text_surface, (box_rect.x + 80, y_offset))
            y_offset += 50
        
        # Menu options - HORIZONTAL LAYOUT
        menu_options = [
            {"text": "PLAY", "color": self.GREEN},
            {"text": "LEADERBOARD", "color": self.YELLOW},
            {"text": "QUIT", "color": self.RED}
        ]
        
        # Menu positioning
        menu_y = 420
        box_width = 220
        box_height = 80
        total_width = (box_width * 3) + (40 * 2)  # 3 boxes + 2 gaps
        start_x = (self.width - total_width) // 2
        
        for i, option in enumerate(menu_options):
            is_selected = (i == selected_index)
            
            # Calculate position
            box_x = start_x + (i * (box_width + 40))
            
            # Highlight selected with animation
            if is_selected:
                pulse = math.sin(self.menu_time * 4) * 3
                border_color = option["color"]
                border_width = 4
                glow_rect = pygame.Rect(box_x - 6, menu_y - 6 - pulse, 
                                       box_width + 12, box_height + 12 + pulse * 2)
                pygame.draw.rect(self.screen, border_color, glow_rect, 
                               border_radius=15, width=border_width)
            
            # Draw box
            opt_rect = pygame.Rect(box_x, menu_y, box_width, box_height)
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            alpha = 240 if is_selected else 180
            pygame.draw.rect(box_surface, (30, 30, 30, alpha), 
                           box_surface.get_rect(), border_radius=12)
            self.screen.blit(box_surface, opt_rect)
            
            # Text centered in box
            text_color = option["color"] if is_selected else self.GRAY
            text_font = self.medium_font if is_selected else self.small_font
            text_surface = text_font.render(option["text"], True, text_color)
            text_rect = text_surface.get_rect(center=(box_x + box_width // 2, menu_y + box_height // 2))
            self.screen.blit(text_surface, text_rect)
        
        # Instructions with icons
        inst_y = menu_y + 100
        
        # Calculate total width for centering
        text_nav = " untuk navigasi • SPASI untuk pilih"
        text_nav_surface = self.small_font.render(text_nav, True, self.GRAY)
        icon_width = 20 if self.icon_exchange else 0
        total_width = icon_width + text_nav_surface.get_width()
        
        start_x = (self.width - total_width) // 2
        
        # Draw exchange icon
        if self.icon_exchange:
            self.screen.blit(self.icon_exchange, (start_x, inst_y))
            start_x += icon_width + 5
        else:
            # Fallback to text
            fallback = self.small_font.render("← →", True, self.GRAY)
            self.screen.blit(fallback, (start_x, inst_y))
            start_x += fallback.get_width()
        
        # Draw rest of text
        self.screen.blit(text_nav_surface, (start_x, inst_y))
        
        # Team info with stylish background
        team_y = self.height - 100
        team_bg = pygame.Surface((self.width, 100), pygame.SRCALPHA)
        pygame.draw.rect(team_bg, (0, 0, 0, 120), team_bg.get_rect())
        self.screen.blit(team_bg, (0, team_y))
        
        team_title = self.small_font.render("Tim Pengembang:", True, self.YELLOW)
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
        
        # Text - use symbol font for better unicode support
        text_surface = self.symbol_font.render(text, True, self.WHITE)
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

    def draw_challenge_header(self, expression_key, y_pos=50):
        """Render the current challenge text with emoji support"""
        if not expression_key:
            return

        from game_logic import GameLogic

        # Access display text (format: "😊 SENYUM LEBAR!")
        game_logic = GameLogic()
        full_text = game_logic.expression_names.get(expression_key, "")
        if not full_text:
            return

        # Try to split emoji from the rest of the text
        emoji_char = None
        label_text = full_text

        if " " in full_text:
            possible_emoji, remainder = full_text.split(" ", 1)
            if not possible_emoji.isascii():
                emoji_char = possible_emoji
                label_text = remainder

        center_x = self.width // 2

        if emoji_char:
            # Render emoji with emoji-capable font
            emoji_surface = self.emoji_font.render(emoji_char, True, self.WHITE)
            text_surface = self.large_font.render(label_text, True, self.YELLOW)

            spacing = 18
            total_width = emoji_surface.get_width() + spacing + text_surface.get_width()
            emoji_pos = (
                center_x - total_width // 2,
                y_pos - emoji_surface.get_height() // 2
            )
            text_pos = (
                emoji_pos[0] + emoji_surface.get_width() + spacing,
                y_pos - text_surface.get_height() // 2
            )

            self.screen.blit(emoji_surface, emoji_pos)
            self.screen.blit(text_surface, text_pos)
        else:
            # Fallback to standard rendering
            text_surface = self.large_font.render(full_text, True, self.YELLOW)
            text_rect = text_surface.get_rect(center=(center_x, y_pos))
            self.screen.blit(text_surface, text_rect)

    def draw_game(self, frame, current_challenge, score, remaining_time):
        """Draw game playing screen"""
        # Draw soft gradient background (purple to dark blue)
        self.draw_gradient_background((25, 20, 45), (15, 25, 50))
        
        # Draw subtle animated particles
        self.update_particles()
        
        # Convert OpenCV frame to Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Mirror horizontally so displayed camera behaves like a mirror
        frame_rgb = np.fliplr(frame_rgb)
        # Pygame surfarray expects (width, height, channels) ordering, so transpose axes
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))

        # Scale and position camera feed
        camera_width = 640
        camera_height = 480
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        frame_surface = pygame.transform.scale(
            frame_surface, (camera_width, camera_height)
        )
        
        # Draw camera border with glow effect
        for i in range(4, 0, -1):
            glow_alpha = 30 - i * 5
            glow_rect = pygame.Rect(camera_x - i * 2, camera_y - i * 2, 
                                   camera_width + i * 4, camera_height + i * 4)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.CYAN, glow_alpha), 
                           glow_surface.get_rect(), border_radius=15)
            self.screen.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
        # Draw camera feed
        self.screen.blit(frame_surface, (camera_x, camera_y))
        
        # Draw camera border
        pygame.draw.rect(self.screen, self.CYAN, 
                        (camera_x, camera_y, camera_width, camera_height), 
                        width=3, border_radius=12)

        # Draw challenge text with emoji support
        self.draw_challenge_header(current_challenge)

        # Draw score with background panel
        score_text = f"Skor: {score}"
        score_bg = pygame.Surface((180, 50), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (30, 25, 50, 200), score_bg.get_rect(), border_radius=10)
        pygame.draw.rect(score_bg, self.GREEN, score_bg.get_rect(), width=2, border_radius=10)
        self.screen.blit(score_bg, (30, 20))
        score_surface = self.medium_font.render(score_text, True, self.GREEN)
        self.screen.blit(score_surface, (50, 30))

        # Draw timer with background panel
        time_text = f"Waktu: {int(remaining_time)}s"
        time_color = self.RED if remaining_time < 5 else self.CYAN
        time_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        border_color = self.RED if remaining_time < 5 else self.CYAN
        pygame.draw.rect(time_bg, (30, 25, 50, 200), time_bg.get_rect(), border_radius=10)
        pygame.draw.rect(time_bg, border_color, time_bg.get_rect(), width=2, border_radius=10)
        time_bg_rect = time_bg.get_rect(topright=(self.width - 30, 20))
        self.screen.blit(time_bg, time_bg_rect)
        time_surface = self.medium_font.render(time_text, True, time_color)
        time_rect = time_surface.get_rect(topright=(self.width - 50, 30))
        self.screen.blit(time_surface, time_rect)

    def draw_game_with_debug(self, frame, current_challenge, score, remaining_time, detected_expression):
        """Draw game playing screen with debug info"""
        # Draw soft gradient background (purple to dark blue)
        self.draw_gradient_background((25, 20, 45), (15, 25, 50))
        
        # Draw subtle animated particles
        self.update_particles()
        
        # Draw floating expression images in background
        self.update_floating_images()

        # Convert OpenCV frame to Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Mirror horizontally so displayed camera behaves like a mirror
        frame_rgb = np.fliplr(frame_rgb)
        # Pygame surfarray expects (width, height, channels) ordering, so transpose axes
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))

        # Scale and position camera feed
        camera_width = 640
        camera_height = 480
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        frame_surface = pygame.transform.scale(
            frame_surface, (camera_width, camera_height)
        )
        
        # Draw camera border with glow effect
        for i in range(4, 0, -1):
            glow_alpha = 30 - i * 5
            glow_rect = pygame.Rect(camera_x - i * 2, camera_y - i * 2, 
                                   camera_width + i * 4, camera_height + i * 4)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.CYAN, glow_alpha), 
                           glow_surface.get_rect(), border_radius=15)
            self.screen.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
        # Draw camera feed
        self.screen.blit(frame_surface, (camera_x, camera_y))
        
        # Draw camera border
        pygame.draw.rect(self.screen, self.CYAN, 
                        (camera_x, camera_y, camera_width, camera_height), 
                        width=3, border_radius=12)

        # Draw animated expression images on both sides
        if current_challenge:
            # Left side - expression image
            left_x = 150
            left_y = 350
            self.draw_animated_expression_image(current_challenge, left_x, left_y)
            
            # Right side - expression image (mirror animation)
            right_x = self.width - 150
            right_y = 350
            self.draw_animated_expression_image(current_challenge, right_x, right_y)

        # Draw challenge text with emoji support
        self.draw_challenge_header(current_challenge)

        # Draw score with background panel
        score_text = f"Skor: {score}"
        score_bg = pygame.Surface((180, 50), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (30, 25, 50, 200), score_bg.get_rect(), border_radius=10)
        pygame.draw.rect(score_bg, self.GREEN, score_bg.get_rect(), width=2, border_radius=10)
        self.screen.blit(score_bg, (30, 20))
        score_surface = self.medium_font.render(score_text, True, self.GREEN)
        self.screen.blit(score_surface, (50, 30))

        # Draw timer with background panel
        time_text = f"Waktu: {int(remaining_time)}s"
        time_color = self.RED if remaining_time < 5 else self.CYAN
        time_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        border_color = self.RED if remaining_time < 5 else self.CYAN
        pygame.draw.rect(time_bg, (30, 25, 50, 200), time_bg.get_rect(), border_radius=10)
        pygame.draw.rect(time_bg, border_color, time_bg.get_rect(), width=2, border_radius=10)
        time_bg_rect = time_bg.get_rect(topright=(self.width - 30, 20))
        self.screen.blit(time_bg, time_bg_rect)
        time_surface = self.medium_font.render(time_text, True, time_color)
        time_rect = time_surface.get_rect(topright=(self.width - 50, 30))
        self.screen.blit(time_surface, time_rect)

        # DEBUG: Draw detected expression
        # detected_text = f"Terdeteksi: {detected_expression}"
        # detected_color = self.GREEN if detected_expression == current_challenge else self.RED
        # detected_surface = self.medium_font.render(detected_text, True, detected_color)
        # self.screen.blit(detected_surface, (50, 70))

        # DEBUG: Draw expression indicator with text
        expression_labels = {
            'happy': 'SENANG',
            'sad': 'SEDIH', 
            'surprised': 'KAGET',
            'neutral': 'NETRAL'
        }
        #(debug expresi)
        # label = expression_labels.get(detected_expression, 'TIDAK DIKETAHUI')
        # emoji_text = f"Ekspresi: {label}"
        # emoji_surface = self.large_font.render(emoji_text, True, self.WHITE)
        # emoji_rect = emoji_surface.get_rect(topright=(self.width - 50, 70))
        # self.screen.blit(emoji_surface, emoji_rect)

    def draw_results(self, score, max_score):
        """Draw enhanced results screen with animations"""
        # Update animation time for effects
        self.menu_time += 0.05
        
        # Animated gradient background
        t = math.sin(self.menu_time * 0.5) * 0.5 + 0.5
        color1 = (int(10 + t * 30), int(5 + t * 20), int(30 + t * 50))
        color2 = (int(40 + t * 40), int(10 + t * 30), int(60 + t * 60))
        self.draw_gradient_background(color1, color2)
        
        # Draw animated particles
        self.update_particles()
        
        # Calculate performance (cap at 100% for display)
        percentage = (score / max_score * 100) if max_score > 0 else 0
        display_percentage = min(percentage, 100)  # Cap at 100% for visual display
        
        # Determine rank and colors
        if percentage >= 80:
            rank = "S"
            rank_color = self.YELLOW
            message = "LUAR BIASA!"
            message_color = self.GREEN
            particle_color = self.YELLOW
            stars_count = 5
        elif percentage >= 60:
            rank = "A"
            rank_color = self.GREEN
            message = "BAGUS SEKALI!"
            message_color = self.BLUE
            particle_color = self.GREEN
            stars_count = 4
        elif percentage >= 40:
            rank = "B"
            rank_color = self.BLUE
            message = "CUKUP BAIK!"
            message_color = self.CYAN
            particle_color = self.BLUE
            stars_count = 3
        else:
            rank = "C"
            rank_color = self.GRAY
            message = "TERUS BERLATIH!"
            message_color = self.WHITE
            particle_color = self.GRAY
            stars_count = 1
        
        # Draw decorative circles with pulse
        pulse = math.sin(self.menu_time * 2) * 15
        for i in range(6):
            alpha = int(20 - i * 3)
            size = int(180 + pulse + i * 35)
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*rank_color, alpha), (size, size), size, 4)
            self.screen.blit(circle_surface, (self.width // 2 - size, 120 - size))
        
        # Animated title with bounce
        bounce = math.sin(self.menu_time * 2.5) * 8
        title_y = 120 + bounce
        
        # Draw "SELESAI!" title with glow
        for i in range(5, 0, -1):
            glow_alpha = 40 - i * 6
            glow_surface = self.title_font.render("SELESAI!", True, (*rank_color, glow_alpha))
            glow_rect = glow_surface.get_rect(center=(self.width // 2, title_y))
            self.screen.blit(glow_surface, glow_rect)
        
        title = self.title_font.render("SELESAI!", True, self.WHITE)
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        self.screen.blit(title, title_rect)
        
        # Draw rank badge with animation
        rank_y = 230
        rank_pulse = math.sin(self.menu_time * 3) * 10
        rank_size = 120 + rank_pulse
        
        # Rank background circle
        rank_bg_surface = pygame.Surface((rank_size * 2, rank_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(rank_bg_surface, (*rank_color, 150), (rank_size, rank_size), rank_size)
        pygame.draw.circle(rank_bg_surface, (*self.WHITE, 200), (rank_size, rank_size), rank_size, 8)
        self.screen.blit(rank_bg_surface, (self.width // 2 - rank_size, rank_y - rank_size))
        
        # Rank text
        rank_font = pygame.font.Font(None, 140)
        rank_surface = rank_font.render(rank, True, self.WHITE)
        rank_rect = rank_surface.get_rect(center=(self.width // 2, rank_y))
        self.screen.blit(rank_surface, rank_rect)
        
        # Draw stars based on performance
        star_y = rank_y + 100
        star_spacing = 60
        total_stars_width = stars_count * star_spacing
        star_start_x = (self.width - total_stars_width) // 2 + star_spacing // 2
        
        for i in range(stars_count):
            star_bounce = math.sin(self.menu_time * 2 + i * 0.5) * 5
            star_x = star_start_x + i * star_spacing
            self.draw_star(star_x, star_y + star_bounce, 20, particle_color)
        
        # Results box - adjusted position and size for better fit
        box_y = rank_y + 160
        box_width = 700
        box_height = 180
        box_rect = pygame.Rect((self.width - box_width) // 2, box_y, box_width, box_height)
        
        # Box glow effect
        for i in range(5, 0, -1):
            glow_alpha = 40 - i * 6
            glow_surface = pygame.Surface((box_width + i * 8, box_height + i * 8), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*rank_color, glow_alpha), glow_surface.get_rect(), border_radius=25)
            self.screen.blit(glow_surface, (box_rect.x - i * 4, box_rect.y - i * 4))
        
        # Box background
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (20, 15, 40, 220), box_surface.get_rect(), border_radius=25)
        pygame.draw.rect(box_surface, rank_color, box_surface.get_rect(), width=4, border_radius=25)
        self.screen.blit(box_surface, box_rect)
        
        # Performance message with glow
        self.draw_text_with_glow(message, self.large_font, message_color, 
                                self.width // 2, box_y + 35)
        
        # Score with animation
        score_pulse = math.sin(self.menu_time * 4) * 3
        score_text = f"SKOR: {score} / {max_score}"
        score_font = pygame.font.Font(None, 48)
        score_surface = score_font.render(score_text, True, self.YELLOW)
        score_rect = score_surface.get_rect(center=(self.width // 2, box_y + 90 + score_pulse))
        
        # Score shadow
        shadow_surface = score_font.render(score_text, True, (20, 20, 40))
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 3, box_y + 93 + score_pulse))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(score_surface, score_rect)
        
        # Percentage bar - FIX: Cap fill_width to not exceed bar_width
        bar_y = box_y + 130
        bar_width = 500
        bar_height = 30
        bar_x = (self.width - bar_width) // 2
        
        # Bar background
        pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=15)
        
        # Filled bar with gradient effect - capped at 100% and rounded
        fill_width = int((display_percentage / 100) * bar_width)
        fill_width = min(fill_width, bar_width)  # Ensure it doesn't exceed bar width
        
        if fill_width > 0:
            # Create a surface for the filled bar with rounded corners
            fill_surface = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)
            
            # Draw gradient on the fill surface
            for i in range(fill_width):
                progress = i / bar_width
                bar_color = (
                    int(rank_color[0] * (1 - progress * 0.3)),
                    int(rank_color[1] * (1 - progress * 0.3)),
                    int(rank_color[2] * (1 - progress * 0.3))
                )
                pygame.draw.line(fill_surface, bar_color, (i, 0), (i, bar_height))
            
            # Create a mask surface with rounded corners
            mask_surface = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)
            pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, fill_width, bar_height), border_radius=15)
            
            # Apply the mask to create rounded fill
            fill_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
            # Draw the rounded filled bar
            self.screen.blit(fill_surface, (bar_x, bar_y))
        
        # Bar border
        pygame.draw.rect(self.screen, self.WHITE, (bar_x, bar_y, bar_width, bar_height), 
                        width=3, border_radius=15)
        
        # Percentage text - show actual percentage even if over 100%
        percent_text = f"{int(percentage)}%"
        percent_surface = self.medium_font.render(percent_text, True, self.WHITE)
        percent_rect = percent_surface.get_rect(center=(self.width // 2, bar_y + bar_height // 2))
        self.screen.blit(percent_surface, percent_rect)
        
        # Control instructions with animation - adjusted position to fit screen
        controls_y = box_y + box_height + 40
        button_pulse = math.sin(self.menu_time * 3) * 8
        
        # Restart button
        restart_y = controls_y
        self.draw_fancy_button("► MAIN LAGI [SPASI]", self.width // 2, restart_y, 
                              self.GREEN, 12 + button_pulse)
        
        # Exit button - adjusted spacing
        exit_y = restart_y + 55
        self.draw_fancy_button("✖ KELUAR [ESC]", self.width // 2, exit_y, 
                              self.RED, 8)
        
        # Floating confetti particles for high scores
        if percentage >= 60:
            self.draw_confetti()
    
    def draw_confetti(self):
        """Draw confetti particles for celebration"""
        for i in range(15):
            x = (self.width // 2) + math.sin(self.menu_time + i) * 400
            y = 100 + ((self.menu_time * 50 + i * 50) % (self.height - 100))
            size = 8 + (i % 3) * 4
            colors = [self.YELLOW, self.PINK, self.CYAN, self.GREEN, self.ORANGE]
            color = colors[i % len(colors)]
            rotation = (self.menu_time * 100 + i * 30) % 360
            
            # Draw rotating rectangle (confetti piece)
            rect_surface = pygame.Surface((size * 2, size), pygame.SRCALPHA)
            rect_surface.fill(color)
            rotated = pygame.transform.rotate(rect_surface, rotation)
            rect_rect = rotated.get_rect(center=(int(x), int(y)))
            self.screen.blit(rotated, rect_rect)
    
    def draw_difficulty_selection(self, selected_index=0):
        """Draw difficulty selection screen"""
        self.draw_gradient_background(self.DARK_PURPLE, self.BLACK)
        self.update_particles()
        
        # Title
        title = self.title_font.render("PILIH KESULITAN", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        
        # Shadow effect
        title_shadow = self.title_font.render("PILIH KESULITAN", True, (50, 50, 50))
        shadow_rect = title_shadow.get_rect(center=(self.width // 2 + 3, 103))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Difficulty options
        difficulties = [
            {
                "name": "MUDAH",
                "desc": "30 detik • 2 ekspresi",
                "color": self.GREEN,
                "emoji": "😊"
            },
            {
                "name": "SEDANG",
                "desc": "20 detik • 4 ekspresi",
                "color": self.YELLOW,
                "emoji": "😐"
            },
            {
                "name": "SULIT",
                "desc": "15 detik • 4 ekspresi • Cepat!",
                "color": self.RED,
                "emoji": "😱"
            }
        ]
        
        y_offset = 220
        for i, diff in enumerate(difficulties):
            is_selected = (i == selected_index)
            
            # Box for difficulty
            box_width = 500
            box_height = 100
            box_x = (self.width - box_width) // 2
            box_y = y_offset + (i * 130)
            
            # Highlight selected
            if is_selected:
                # Animated border
                border_color = diff["color"]
                border_width = 5
                glow_rect = pygame.Rect(box_x - 10, box_y - 10, 
                                       box_width + 20, box_height + 20)
                pygame.draw.rect(self.screen, border_color, glow_rect, 
                               border_radius=15, width=border_width)
            
            # Draw box
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surface, (30, 30, 30, 230), 
                           box_surface.get_rect(), border_radius=15)
            self.screen.blit(box_surface, box_rect)
            
            # Difficulty name
            name_surface = self.large_font.render(diff["name"], True, diff["color"])
            name_rect = name_surface.get_rect(left=box_x + 30, centery=box_y + 35)
            self.screen.blit(name_surface, name_rect)
            
            # Description
            desc_surface = self.small_font.render(diff["desc"], True, self.WHITE)
            desc_rect = desc_surface.get_rect(left=box_x + 30, centery=box_y + 70)
            self.screen.blit(desc_surface, desc_rect)
            
            # Emoji - using emoji font
            emoji_surface = self.emoji_font.render(diff["emoji"], True, self.WHITE)
            emoji_rect = emoji_surface.get_rect(right=box_x + box_width - 30, 
                                               centery=box_y + 50)
            self.screen.blit(emoji_surface, emoji_rect)
        
        # Instructions with icon
        inst_y = self.height - 50
        
        # Calculate components
        text_pilih = " untuk pilih • SPASI untuk mulai • L untuk Leaderboard • ESC untuk keluar"
        text_pilih_surface = self.small_font.render(text_pilih, True, self.GRAY)
        icon_width = 20 if self.icon_up_down else 0
        total_width = icon_width + text_pilih_surface.get_width()
        
        start_x = (self.width - total_width) // 2
        
        # Draw up-down icon
        if self.icon_up_down:
            self.screen.blit(self.icon_up_down, (start_x, inst_y))
            start_x += icon_width + 5
        else:
            # Fallback to text
            fallback = self.small_font.render("↑↓", True, self.GRAY)
            self.screen.blit(fallback, (start_x, inst_y))
            start_x += fallback.get_width()
        
        # Draw rest of text
        self.screen.blit(text_pilih_surface, (start_x, inst_y))
    
    def draw_leaderboard(self, leaderboard_manager, difficulty="medium"):
        """Draw leaderboard screen"""
        self.draw_gradient_background(self.DARK_PURPLE, self.BLACK)
        self.update_particles()
        
        # Title
        title = self.title_font.render("LEADERBOARD", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Difficulty tabs
        difficulties = ["easy", "medium", "hard"]
        diff_names = {"easy": "MUDAH", "medium": "SEDANG", "hard": "SULIT"}
        diff_colors = {"easy": self.GREEN, "medium": self.YELLOW, "hard": self.RED}
        
        tab_y = 150
        tab_width = 200
        tab_spacing = 220
        start_x = (self.width - (len(difficulties) * tab_spacing - 20)) // 2
        
        for i, diff in enumerate(difficulties):
            tab_x = start_x + (i * tab_spacing)
            is_active = (diff == difficulty)
            
            # Draw tab
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 50)
            tab_color = diff_colors[diff] if is_active else self.GRAY
            
            if is_active:
                pygame.draw.rect(self.screen, tab_color, tab_rect, border_radius=10)
                text_color = self.BLACK
            else:
                pygame.draw.rect(self.screen, tab_color, tab_rect, 
                               border_radius=10, width=3)
                text_color = tab_color
            
            tab_text = self.medium_font.render(diff_names[diff], True, text_color)
            tab_text_rect = tab_text.get_rect(center=tab_rect.center)
            self.screen.blit(tab_text, tab_text_rect)
        
        # Get top scores
        scores = leaderboard_manager.get_top_scores(difficulty, 10)
        
        # Draw scores table
        table_y = 230
        if scores:
            for i, entry in enumerate(scores):
                rank_y = table_y + (i * 45)
                
                # Rank colors
                if i == 0:
                    rank_color = self.YELLOW  # Gold
                elif i == 1:
                    rank_color = self.LIGHT_BLUE  # Silver
                elif i == 2:
                    rank_color = self.ORANGE  # Bronze
                else:
                    rank_color = self.WHITE
                
                # Rank
                rank_text = f"#{i + 1}"
                rank_surface = self.medium_font.render(rank_text, True, rank_color)
                self.screen.blit(rank_surface, (150, rank_y))
                
                # Name
                name_surface = self.medium_font.render(entry["name"], True, self.WHITE)
                self.screen.blit(name_surface, (250, rank_y))
                
                # Score
                score_text = f"{entry['score']} poin"
                score_surface = self.medium_font.render(score_text, True, self.GREEN)
                self.screen.blit(score_surface, (550, rank_y))
                
                # Date
                date_surface = self.small_font.render(entry["date"], True, self.GRAY)
                self.screen.blit(date_surface, (800, rank_y + 5))
        else:
            # No scores yet
            no_scores = "Belum ada skor tercatat"
            no_scores_surface = self.large_font.render(no_scores, True, self.GRAY)
            no_scores_rect = no_scores_surface.get_rect(center=(self.width // 2, 400))
            self.screen.blit(no_scores_surface, no_scores_rect)
        
        # Instructions
        instructions = "1/2/3 untuk ganti difficulty • ESC untuk kembali"
        inst_surface = self.small_font.render(instructions, True, self.GRAY)
        inst_rect = inst_surface.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(inst_surface, inst_rect)
    
    def draw_name_input(self, current_name=""):
        """Draw name input screen"""
        self.draw_gradient_background(self.DARK_PURPLE, self.BLACK)
        self.update_particles()
        
        # Title
        title = self.title_font.render("MASUKKAN NAMA", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        
        # Shadow
        title_shadow = self.title_font.render("MASUKKAN NAMA", True, (50, 50, 50))
        shadow_rect = title_shadow.get_rect(center=(self.width // 2 + 3, 153))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = "Nama kamu akan muncul di leaderboard!"
        subtitle_surface = self.medium_font.render(subtitle, True, self.LIGHT_BLUE)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 220))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Input box
        box_width = 600
        box_height = 80
        box_x = (self.width - box_width) // 2
        box_y = 300
        
        # Box background with border
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, self.YELLOW, box_rect, border_radius=15, width=4)
        
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (40, 40, 40, 240), 
                        box_surface.get_rect(), border_radius=15)
        self.screen.blit(box_surface, box_rect)
        
        # Display current name or placeholder
        display_text = current_name if current_name else "Ketik nama kamu..."
        text_color = self.WHITE if current_name else self.GRAY
        name_surface = self.large_font.render(display_text, True, text_color)
        name_rect = name_surface.get_rect(center=(self.width // 2, box_y + 40))
        self.screen.blit(name_surface, name_rect)
        
        # Blinking cursor
        if current_name and int(pygame.time.get_ticks() / 500) % 2:
            cursor_x = name_rect.right + 10
            cursor_y = box_y + 20
            pygame.draw.rect(self.screen, self.WHITE, (cursor_x, cursor_y, 3, 40))
        
        # Character limit indicator
        limit_text = f"{len(current_name)}/15 karakter"
        limit_color = self.RED if len(current_name) >= 15 else self.GRAY
        limit_surface = self.small_font.render(limit_text, True, limit_color)
        limit_rect = limit_surface.get_rect(center=(self.width // 2, box_y + box_height + 30))
        self.screen.blit(limit_surface, limit_rect)
        
        # Instructions
        instructions = [
            "Ketik nama kamu (A-Z, 0-9, spasi)",
            "ENTER untuk lanjut • BACKSPACE untuk hapus • ESC untuk skip"
        ]
        
        inst_y = 450
        for inst in instructions:
            inst_surface = self.small_font.render(inst, True, self.GRAY)
            inst_rect = inst_surface.get_rect(center=(self.width // 2, inst_y))
            self.screen.blit(inst_surface, inst_rect)
            inst_y += 35
        
        # Example names suggestion
        examples = "Contoh: Player1, Falih, GamerPro"
        example_surface = self.small_font.render(examples, True, self.CYAN)
        example_rect = example_surface.get_rect(center=(self.width // 2, 550))
        self.screen.blit(example_surface, example_rect)
