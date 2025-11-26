"""
Image Manager - Handles expression images and rendering
"""

import os
import sys
import math
import pygame


def get_base_path():
    """Get base path for assets"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ImageManager:
    """Manages expression images and rendering"""
    
    def __init__(self, image_size=200):
        """
        Initialize image manager
        
        Args:
            image_size: Size of expression images in pixels
        """
        self.image_size = image_size
        self.expression_images = {}
        self.animation_time = 0
        self.load_expression_images()
    
    def load_expression_images(self):
        """Load expression images from assets folder"""
        # Mapping from game expressions to photo filenames
        image_mapping = {
            "happy": "Senang.png",
            "sad": "Sedih.png",
            "surprised": "Kaget.png",
            "neutral": "Datar.png"
        }
        
        # Get path to assets folder
        base_path = os.path.join(get_base_path(), "assets", "photo")
        
        for expression, filename in image_mapping.items():
            image_path = os.path.join(base_path, filename)
            try:
                # Load and scale image
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (self.image_size, self.image_size))
                self.expression_images[expression] = image
                print(f"✓ Loaded {expression} image: {filename}")
            except Exception as e:
                print(f"✗ Failed to load {expression} image: {e}")
                # Create placeholder if image fails to load
                placeholder = pygame.Surface((self.image_size, self.image_size))
                placeholder.fill((155, 89, 182))  # Purple
                self.expression_images[expression] = placeholder
    
    def get_expression_images(self):
        """Get dictionary of loaded expression images"""
        return self.expression_images
    
    def draw_animated_expression_image(self, screen, expression, x, y, colors):
        """
        Draw expression image with swaying animation
        
        Args:
            screen: Pygame screen surface
            expression: Expression key
            x: X position
            y: Y position
            colors: Colors instance for glow effects
        """
        if expression not in self.expression_images:
            return
        
        # Update animation time
        self.animation_time += 0.1
        
        # Calculate swaying motion (left-right)
        sway_amount = 30
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
                glow_color = (*colors.YELLOW, alpha)
            elif expression == "sad":
                glow_color = (*colors.BLUE, alpha)
            elif expression == "surprised":
                glow_color = (*colors.ORANGE, alpha)
            else:  # neutral
                glow_color = (*colors.GRAY, alpha)
            
            pygame.draw.rect(temp_surface, glow_color, temp_surface.get_rect(), border_radius=20)
            glow_surface.blit(temp_surface, (20 - i * 4, 20 - i * 4))
        
        # Draw glow
        screen.blit(glow_surface, (final_x - 20, final_y - 20))
        
        # Draw the image
        screen.blit(rotated_image, (final_x, final_y))
