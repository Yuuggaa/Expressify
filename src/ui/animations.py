"""
Animations - Particle systems and animation effects
"""

import random
import math
import pygame


class Particle:
    """Single particle for background effects"""
    
    def __init__(self, x, y, size, speed, color, direction):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = direction


class ParticleSystem:
    """Manages background particles"""
    
    def __init__(self, width, height, colors, particle_count=30):
        """
        Initialize particle system
        
        Args:
            width: Screen width
            height: Screen height
            colors: Colors instance
            particle_count: Number of particles to create
        """
        self.width = width
        self.height = height
        self.colors = colors
        self.particles = []
        self.init_particles(particle_count)
    
    def init_particles(self, count):
        """Initialize floating particles for background"""
        color_choices = [
            self.colors.PURPLE, self.colors.PINK, self.colors.CYAN,
            self.colors.ORANGE, self.colors.YELLOW, self.colors.LIGHT_BLUE
        ]
        
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(3, 12),
                'speed': random.uniform(0.5, 2),
                'color': random.choice(color_choices),
                'direction': random.uniform(0, 2 * math.pi)
            })
    
    def update_and_draw(self, screen):
        """Update and draw all particles"""
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
                alpha_surface = pygame.Surface(
                    (particle['size'] * i * 2, particle['size'] * i * 2), 
                    pygame.SRCALPHA
                )
                color_with_alpha = (*particle['color'], 50 // i)
                pygame.draw.circle(
                    alpha_surface, color_with_alpha,
                    (particle['size'] * i, particle['size'] * i),
                    particle['size'] * i
                )
                screen.blit(
                    alpha_surface,
                    (int(particle['x']) - particle['size'] * i,
                     int(particle['y']) - particle['size'] * i)
                )


class FloatingImage:
    """Floating expression image for background"""
    
    def __init__(self, expression, x, y, size, speed, direction, rotation, rotation_speed, alpha, bob_offset):
        self.expression = expression
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.rotation_speed = rotation_speed
        self.alpha = alpha
        self.bob_offset = bob_offset
    
    def update(self, width, height):
        """Update floating image position"""
        # Update position
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Wrap around screen
        if self.x < -100:
            self.x = width + 100
        elif self.x > width + 100:
            self.x = -100
        if self.y < -100:
            self.y = height + 100
        elif self.y > height + 100:
            self.y = -100
        
        # Update rotation
        self.rotation += self.rotation_speed


class FloatingImageSystem:
    """Manages floating expression images"""
    
    def __init__(self, width, height, image_count=8):
        """
        Initialize floating image system
        
        Args:
            width: Screen width
            height: Screen height
            image_count: Number of floating images
        """
        self.width = width
        self.height = height
        self.floating_images = []
        self.animation_time = 0
        self.init_floating_images(image_count)
    
    def init_floating_images(self, count):
        """Initialize floating expression images"""
        expressions = ["happy", "sad", "surprised", "neutral"]
        for _ in range(count):
            expression = random.choice(expressions)
            self.floating_images.append(
                FloatingImage(
                    expression=expression,
                    x=random.randint(0, self.width),
                    y=random.randint(0, self.height),
                    size=random.randint(40, 80),
                    speed=random.uniform(0.3, 0.8),
                    direction=random.uniform(0, 2 * math.pi),
                    rotation=random.uniform(0, 360),
                    rotation_speed=random.uniform(-2, 2),
                    alpha=random.randint(30, 80),
                    bob_offset=random.uniform(0, 2 * math.pi)
                )
            )
    
    def update_and_draw(self, screen, expression_images, exclude_area=None):
        """
        Update and draw floating images
        
        Args:
            screen: Pygame screen surface
            expression_images: Dictionary of expression images
            exclude_area: Optional tuple (x, y, width, height) to exclude from rendering
        """
        self.animation_time += 0.1
        
        for img in self.floating_images:
            img.update(self.width, self.height)
            
            # Check if image is in excluded area (e.g., camera feed area)
            if exclude_area:
                ex, ey, ew, eh = exclude_area
                # Add margin to avoid images appearing at the edge
                margin = 50
                if (ex - margin <= img.x <= ex + ew + margin and 
                    ey - margin <= img.y <= ey + eh + margin):
                    continue  # Skip rendering this image
            
            # Get expression image
            if img.expression in expression_images:
                original_image = expression_images[img.expression]
                
                # Scale down the image
                small_image = pygame.transform.scale(original_image, (img.size, img.size))
                
                # Apply rotation
                rotated_image = pygame.transform.rotate(small_image, img.rotation)
                
                # Create surface with alpha for transparency
                alpha_surface = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
                alpha_surface.blit(rotated_image, (0, 0))
                alpha_surface.set_alpha(img.alpha)
                
                # Add bobbing motion
                bob = math.sin(self.animation_time * 0.5 + img.bob_offset) * 8
                
                # Draw the floating image
                final_x = int(img.x - rotated_image.get_width() // 2)
                final_y = int(img.y + bob - rotated_image.get_height() // 2)
                screen.blit(alpha_surface, (final_x, final_y))


class ConfettiSystem:
    """Confetti animation for celebrations"""
    
    def __init__(self, width, height, colors):
        """
        Initialize confetti system
        
        Args:
            width: Screen width
            height: Screen height
            colors: Colors instance
        """
        self.width = width
        self.height = height
        self.colors = colors
        self.animation_time = 0
    
    def update_and_draw(self, screen):
        """Draw confetti particles"""
        self.animation_time += 0.05
        
        for i in range(15):
            x = (self.width // 2) + math.sin(self.animation_time + i) * 400
            y = 100 + ((self.animation_time * 50 + i * 50) % (self.height - 100))
            size = 8 + (i % 3) * 4
            colors = [
                self.colors.YELLOW, self.colors.PINK, self.colors.CYAN,
                self.colors.GREEN, self.colors.ORANGE
            ]
            color = colors[i % len(colors)]
            rotation = (self.animation_time * 100 + i * 30) % 360
            
            # Draw rotating rectangle (confetti piece)
            rect_surface = pygame.Surface((size * 2, size), pygame.SRCALPHA)
            rect_surface.fill(color)
            rotated = pygame.transform.rotate(rect_surface, rotation)
            rect_rect = rotated.get_rect(center=(int(x), int(y)))
            screen.blit(rotated, rect_rect)
