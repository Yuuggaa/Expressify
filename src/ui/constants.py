"""
UI Constants - Colors, dimensions, and configuration values
"""

import pygame


class Colors:
    """Color palette for the UI"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (50, 255, 130)
    RED = (255, 69, 96)
    BLUE = (64, 156, 255)
    YELLOW = (255, 220, 50)
    PURPLE = (155, 89, 182)
    ORANGE = (255, 159, 64)
    PINK = (255, 105, 180)
    CYAN = (64, 224, 208)
    GRAY = (128, 128, 128)
    DARK_PURPLE = (45, 20, 70)
    LIGHT_BLUE = (135, 206, 250)


class Dimensions:
    """Dimension constants for UI elements"""
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    IMAGE_SIZE = 200  # Expression image size
    BOX_BORDER_RADIUS = 15
    BUTTON_BORDER_RADIUS = 25


class FontManager:
    """Manages font loading and caching"""
    
    def __init__(self):
        """Initialize fonts"""
        # Try to load system fonts that support emoji
        try:
            self.emoji_font = pygame.font.SysFont('segoeuiemoji', 72)
            self.symbol_font = pygame.font.SysFont('segoeuiemoji', 28)
        except:
            try:
                self.emoji_font = pygame.font.SysFont('seguisym', 72)
                self.symbol_font = pygame.font.SysFont('seguisym', 28)
            except:
                self.emoji_font = pygame.font.Font(None, 72)
                self.symbol_font = pygame.font.Font(None, 28)
        
        self.title_font = pygame.font.Font(None, 92)
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
    
    def get_emoji_font(self):
        return self.emoji_font
    
    def get_symbol_font(self):
        return self.symbol_font
    
    def get_title_font(self):
        return self.title_font
    
    def get_large_font(self):
        return self.large_font
    
    def get_medium_font(self):
        return self.medium_font
    
    def get_small_font(self):
        return self.small_font
