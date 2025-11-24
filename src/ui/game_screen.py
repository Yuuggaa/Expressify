"""
Game Screen - Game playing screen rendering
"""

import cv2
import numpy as np
import pygame


class GameScreen:
    """Renders the game playing screen"""
    
    def __init__(self, renderer, colors, fonts, width, height, dimensions):
        """
        Initialize game screen
        
        Args:
            renderer: UIRenderer instance
            colors: Colors instance
            fonts: FontManager instance
            width: Screen width
            height: Screen height
            dimensions: Dimensions instance
        """
        self.renderer = renderer
        self.colors = colors
        self.fonts = fonts
        self.width = width
        self.height = height
        self.dimensions = dimensions
    
    def draw(self, screen, frame, current_challenge, score, remaining_time):
        """Draw game playing screen"""
        # Draw soft gradient background
        self.renderer.draw_gradient_background((25, 20, 45), (15, 25, 50))
        
        # Convert and draw camera feed
        self._draw_camera_feed(screen, frame)
        
        # Draw challenge text
        self._draw_challenge_header(screen, current_challenge)
        
        # Draw score panel
        self._draw_score_panel(screen, score)
        
        # Draw timer panel
        self._draw_timer_panel(screen, remaining_time)
    
    def draw_with_debug(self, screen, frame, current_challenge, score, remaining_time, 
                       detected_expression, image_manager):
        """Draw game screen with debug info and animated images"""
        # Draw soft gradient background
        self.renderer.draw_gradient_background((25, 20, 45), (15, 25, 50))
        
        # Convert and draw camera feed
        self._draw_camera_feed(screen, frame)
        
        # Draw animated expression images on both sides
        if current_challenge and image_manager:
            left_x = 150
            left_y = 350
            image_manager.draw_animated_expression_image(
                screen, current_challenge, left_x, left_y, self.colors
            )
            
            right_x = self.width - 150
            right_y = 350
            image_manager.draw_animated_expression_image(
                screen, current_challenge, right_x, right_y, self.colors
            )
        
        # Draw challenge text
        self._draw_challenge_header(screen, current_challenge)
        
        # Draw score panel
        self._draw_score_panel(screen, score)
        
        # Draw timer panel
        self._draw_timer_panel(screen, remaining_time)
    
    def get_camera_area(self):
        """
        Get the camera feed area coordinates
        
        Returns:
            tuple: (x, y, width, height) of camera area
        """
        camera_width = self.dimensions.CAMERA_WIDTH
        camera_height = self.dimensions.CAMERA_HEIGHT
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        return (camera_x, camera_y, camera_width, camera_height)
    
    def _draw_camera_feed(self, screen, frame):
        """Draw camera feed with border"""
        # Convert OpenCV frame to Pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.fliplr(frame_rgb)  # Mirror horizontally
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
        
        # Scale and position
        camera_width = self.dimensions.CAMERA_WIDTH
        camera_height = self.dimensions.CAMERA_HEIGHT
        camera_x = (self.width - camera_width) // 2
        camera_y = 120
        frame_surface = pygame.transform.scale(frame_surface, (camera_width, camera_height))
        
        # Draw border glow
        for i in range(4, 0, -1):
            glow_alpha = 30 - i * 5
            glow_rect = pygame.Rect(
                camera_x - i * 2, camera_y - i * 2,
                camera_width + i * 4, camera_height + i * 4
            )
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surface, (*self.colors.CYAN, glow_alpha),
                glow_surface.get_rect(), border_radius=15
            )
            screen.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
        # Draw camera feed
        screen.blit(frame_surface, (camera_x, camera_y))
        
        # Draw border
        pygame.draw.rect(
            screen, self.colors.CYAN,
            (camera_x, camera_y, camera_width, camera_height),
            width=3, border_radius=12
        )
    
    def _draw_challenge_header(self, screen, expression_key):
        """Draw challenge text with emoji support"""
        if not expression_key:
            return
        
        from game_logic import GameLogic
        
        game_logic = GameLogic()
        full_text = game_logic.expression_names.get(expression_key, "")
        if not full_text:
            return
        
        # Try to split emoji from text
        emoji_char = None
        label_text = full_text
        
        if " " in full_text:
            possible_emoji, remainder = full_text.split(" ", 1)
            if not possible_emoji.isascii():
                emoji_char = possible_emoji
                label_text = remainder
        
        center_x = self.width // 2
        y_pos = 50
        
        if emoji_char:
            emoji_surface = self.fonts.get_emoji_font().render(emoji_char, True, self.colors.WHITE)
            text_surface = self.fonts.get_large_font().render(label_text, True, self.colors.YELLOW)
            
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
            
            screen.blit(emoji_surface, emoji_pos)
            screen.blit(text_surface, text_pos)
        else:
            text_surface = self.fonts.get_large_font().render(full_text, True, self.colors.YELLOW)
            text_rect = text_surface.get_rect(center=(center_x, y_pos))
            screen.blit(text_surface, text_rect)
    
    def _draw_score_panel(self, screen, score):
        """Draw score panel"""
        score_text = f"Skor: {score}"
        score_bg = pygame.Surface((180, 50), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (30, 25, 50, 200), score_bg.get_rect(), border_radius=10)
        pygame.draw.rect(score_bg, self.colors.GREEN, score_bg.get_rect(), width=2, border_radius=10)
        screen.blit(score_bg, (30, 20))
        
        score_surface = self.fonts.get_medium_font().render(score_text, True, self.colors.GREEN)
        screen.blit(score_surface, (50, 30))
    
    def _draw_timer_panel(self, screen, remaining_time):
        """Draw timer panel"""
        time_text = f"Waktu: {int(remaining_time)}s"
        time_color = self.colors.RED if remaining_time < 5 else self.colors.CYAN
        time_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        border_color = self.colors.RED if remaining_time < 5 else self.colors.CYAN
        
        pygame.draw.rect(time_bg, (30, 25, 50, 200), time_bg.get_rect(), border_radius=10)
        pygame.draw.rect(time_bg, border_color, time_bg.get_rect(), width=2, border_radius=10)
        
        time_bg_rect = time_bg.get_rect(topright=(self.width - 30, 20))
        screen.blit(time_bg, time_bg_rect)
        
        time_surface = self.fonts.get_medium_font().render(time_text, True, time_color)
        time_rect = time_surface.get_rect(topright=(self.width - 50, 30))
        screen.blit(time_surface, time_rect)
