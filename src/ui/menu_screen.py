"""
Menu Screen - Main menu rendering
"""

import math
import pygame
import os
import sys


def get_base_path():
    """Get base path for assets"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class MenuScreen:
    """Renders the main menu screen"""
    
    def __init__(self, renderer, colors, fonts, width, height):
        """
        Initialize menu screen
        
        Args:
            renderer: UIRenderer instance
            colors: Colors instance
            fonts: FontManager instance
            width: Screen width
            height: Screen height
        """
        self.renderer = renderer
        self.colors = colors
        self.fonts = fonts
        self.width = width
        self.height = height
        self.menu_time = 0
        
        # Load icon images
        self.load_icons()
    
    def load_icons(self):
        """Load UI icons"""
        # Get path to assets folder
        images_dir = os.path.join(get_base_path(), "assets", "images")
        
        try:
            self.icon_exchange = pygame.image.load(os.path.join(images_dir, "exchange.png"))
            self.icon_exchange = pygame.transform.scale(self.icon_exchange, (20, 20))
        except Exception as e:
            print(f"⚠ Failed to load exchange icon: {e}")
            self.icon_exchange = None
    
    def draw(self, screen, selected_index=0):
        """Draw main menu screen"""
        self.menu_time += 0.05
        
        # Animated gradient background
        t = math.sin(self.menu_time * 0.5) * 0.5 + 0.5
        color1 = (int(20 + t * 20), int(10 + t * 30), int(40 + t * 40))
        color2 = (int(60 + t * 30), int(20 + t * 20), int(80 + t * 40))
        self.renderer.draw_gradient_background(color1, color2)
        
        # Draw decorative circles
        pulse = math.sin(self.menu_time) * 20
        for i in range(5):
            alpha = int(30 - i * 5)
            size = int(150 + pulse + i * 30)
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*self.colors.PURPLE, alpha), (size, size), size, 3)
            screen.blit(circle_surface, (self.width // 2 - size, 150 - size))
        
        # Animated title with bounce effect
        bounce = math.sin(self.menu_time * 2) * 10
        title_y = 150 + bounce
        
        # Draw title with rainbow gradient effect
        self._draw_rainbow_title(screen, "EXPRESSIFY", title_y)
        
        # Subtitle with glow
        subtitle_y = 240
        self.renderer.draw_text_with_glow(
            "Face Expression Game", 
            self.fonts.get_medium_font(),
            self.colors.CYAN, 
            self.width // 2, 
            subtitle_y
        )
        
        # Decorative stars
        emoji_bounce = math.sin(self.menu_time * 1.5) * 5
        self.renderer.draw_star(200, subtitle_y + emoji_bounce, 25, self.colors.YELLOW)
        self.renderer.draw_star(self.width - 200, subtitle_y - emoji_bounce, 25, self.colors.PINK)
        
        # Instructions box
        self._draw_instructions_box(screen)
        
        # Menu options
        self._draw_menu_options(screen, selected_index)
        
        # Navigation instructions
        self._draw_navigation_instructions(screen)
        
        # Team info
        self._draw_team_info(screen)
    
    def _draw_rainbow_title(self, screen, title_text, title_y):
        """Draw title with rainbow effect"""
        char_surfaces = []
        total_width = 0
        
        for i, char in enumerate(title_text):
            hue = (self.menu_time * 50 + i * 30) % 360
            color = self.renderer.hsv_to_rgb(hue, 100, 100)
            char_surface = self.fonts.get_title_font().render(char, True, color)
            char_surfaces.append(char_surface)
            total_width += char_surface.get_width()
        
        x_offset = (self.width - total_width) // 2
        for i, char_surface in enumerate(char_surfaces):
            char_bounce = math.sin(self.menu_time * 2 + i * 0.3) * 8
            shadow = self.fonts.get_title_font().render(title_text[i], True, (20, 20, 40))
            screen.blit(shadow, (x_offset + 4, title_y + char_bounce + 4))
            screen.blit(char_surface, (x_offset, title_y + char_bounce))
            x_offset += char_surface.get_width()
    
    def _draw_instructions_box(self, screen):
        """Draw instructions box"""
        box_y = 340
        box_height = 220
        box_rect = pygame.Rect(self.width // 2 - 400, box_y, 800, box_height)
        
        # Draw box with border glow
        for i in range(5, 0, -1):
            alpha = 50 - i * 8
            border_surface = pygame.Surface(
                (box_rect.width + i * 4, box_rect.height + i * 4), 
                pygame.SRCALPHA
            )
            pygame.draw.rect(
                border_surface, 
                (*self.colors.PURPLE, alpha),
                border_surface.get_rect(), 
                border_radius=20
            )
            screen.blit(border_surface, (box_rect.x - i * 2, box_rect.y - i * 2))
        
        # Box background
        box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (30, 20, 50, 180), box_surface.get_rect(), border_radius=20)
        screen.blit(box_surface, box_rect)
        
        # Instructions
        instructions = ["Tunjukkan ekspresi wajah sesuai instruksi!"]
        y_offset = box_y + 20
        
        for text in instructions:
            # Decorative bullet
            pygame.draw.circle(screen, self.colors.YELLOW, (box_rect.x + 50, y_offset + 10), 8)
            pygame.draw.circle(screen, self.colors.WHITE, (box_rect.x + 50, y_offset + 10), 4)
            
            text_surface = self.fonts.get_small_font().render(text, True, self.colors.WHITE)
            screen.blit(text_surface, (box_rect.x + 80, y_offset))
            y_offset += 50
    
    def _draw_menu_options(self, screen, selected_index):
        """Draw menu options"""
        menu_options = [
            {"text": "PLAY", "color": self.colors.GREEN},
            {"text": "LEADERBOARD", "color": self.colors.YELLOW},
            {"text": "QUIT", "color": self.colors.RED}
        ]
        
        menu_y = 420
        box_width = 220
        box_height = 80
        total_width = (box_width * 3) + (40 * 2)
        start_x = (self.width - total_width) // 2
        
        for i, option in enumerate(menu_options):
            is_selected = (i == selected_index)
            box_x = start_x + (i * (box_width + 40))
            
            # Highlight selected
            if is_selected:
                pulse = math.sin(self.menu_time * 4) * 3
                glow_rect = pygame.Rect(
                    box_x - 6, menu_y - 6 - pulse,
                    box_width + 12, box_height + 12 + pulse * 2
                )
                pygame.draw.rect(
                    screen, option["color"], glow_rect,
                    border_radius=15, width=4
                )
            
            # Draw box
            opt_rect = pygame.Rect(box_x, menu_y, box_width, box_height)
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            alpha = 240 if is_selected else 180
            pygame.draw.rect(
                box_surface, (30, 30, 30, alpha),
                box_surface.get_rect(), border_radius=12
            )
            screen.blit(box_surface, opt_rect)
            
            # Text
            text_color = option["color"] if is_selected else self.colors.GRAY
            text_font = self.fonts.get_medium_font() if is_selected else self.fonts.get_small_font()
            text_surface = text_font.render(option["text"], True, text_color)
            text_rect = text_surface.get_rect(center=(box_x + box_width // 2, menu_y + box_height // 2))
            screen.blit(text_surface, text_rect)
    
    def _draw_navigation_instructions(self, screen):
        """Draw navigation instructions"""
        inst_y = 520
        text_nav = " untuk navigasi • SPASI untuk pilih"
        text_nav_surface = self.fonts.get_small_font().render(text_nav, True, self.colors.GRAY)
        icon_width = 20 if self.icon_exchange else 0
        total_width = icon_width + text_nav_surface.get_width()
        start_x = (self.width - total_width) // 2
        
        if self.icon_exchange:
            screen.blit(self.icon_exchange, (start_x, inst_y))
            start_x += icon_width + 5
        else:
            fallback = self.fonts.get_small_font().render("← →", True, self.colors.GRAY)
            screen.blit(fallback, (start_x, inst_y))
            start_x += fallback.get_width()
        
        screen.blit(text_nav_surface, (start_x, inst_y))
    
    def _draw_team_info(self, screen):
        """Draw team information"""
        team_y = self.height - 100
        team_bg = pygame.Surface((self.width, 100), pygame.SRCALPHA)
        pygame.draw.rect(team_bg, (0, 0, 0, 120), team_bg.get_rect())
        screen.blit(team_bg, (0, team_y))
        
        team_title = self.fonts.get_small_font().render("Tim Pengembang:", True, self.colors.YELLOW)
        team_rect = team_title.get_rect(center=(self.width // 2, team_y + 25))
        screen.blit(team_title, team_rect)
        
        members = "Falih Dzakwan Zuhdi • Hamka Putra Andiyan • Bayu Ega Ferdana"
        text = self.fonts.get_small_font().render(members, True, self.colors.LIGHT_BLUE)
        text_rect = text.get_rect(center=(self.width // 2, team_y + 60))
        screen.blit(text, text_rect)
