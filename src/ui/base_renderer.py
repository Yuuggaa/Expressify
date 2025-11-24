"""
Base UI Components - Common rendering utilities
"""

import pygame
import colorsys


class UIRenderer:
    """Base class for UI rendering utilities"""
    
    def __init__(self, screen, colors, fonts):
        """
        Initialize UI renderer
        
        Args:
            screen: Pygame screen surface
            colors: Colors instance
            fonts: FontManager instance
        """
        self.screen = screen
        self.colors = colors
        self.fonts = fonts
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_gradient_background(self, color1, color2):
        """Draw a vertical gradient background"""
        for y in range(self.height):
            progress = y / self.height
            r = int(color1[0] * (1 - progress) + color2[0] * progress)
            g = int(color1[1] * (1 - progress) + color2[1] * progress)
            b = int(color1[2] * (1 - progress) + color2[2] * progress)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
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
        text_surface = self.fonts.get_symbol_font().render(text, True, self.colors.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV color to RGB"""
        r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def draw_star(self, x, y, size, color):
        """Draw a star shape"""
        import math
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
        pygame.draw.polygon(self.screen, self.colors.WHITE, points, 2)
