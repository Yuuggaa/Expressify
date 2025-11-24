"""
Difficulty and Other Screens - Additional game screens
"""

import os
import math
import pygame


class DifficultyScreen:
    """Renders difficulty selection screen"""
    
    def __init__(self, renderer, colors, fonts, width, height):
        """
        Initialize difficulty screen
        
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
        
        # Load icon
        self.load_icons()
    
    def load_icons(self):
        """Load UI icons"""
        # Get path to assets folder (up from ui/ to src/ to root/ then to assets/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        root_dir = os.path.dirname(src_dir)
        images_dir = os.path.join(root_dir, "assets", "images")
        
        try:
            self.icon_up_down = pygame.image.load(os.path.join(images_dir, "up-down.png"))
            self.icon_up_down = pygame.transform.scale(self.icon_up_down, (20, 20))
        except Exception as e:
            print(f"⚠ Failed to load up-down icon: {e}")
            self.icon_up_down = None
    
    def draw(self, screen, selected_index=0):
        """Draw difficulty selection screen"""
        self.renderer.draw_gradient_background(self.colors.DARK_PURPLE, self.colors.BLACK)
        
        # Title
        title = self.fonts.get_title_font().render("PILIH KESULITAN", True, self.colors.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        
        # Shadow
        title_shadow = self.fonts.get_title_font().render("PILIH KESULITAN", True, (50, 50, 50))
        shadow_rect = title_shadow.get_rect(center=(self.width // 2 + 3, 103))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title, title_rect)
        
        # Difficulty options
        difficulties = [
            {
                "name": "MUDAH",
                "desc": "30 detik • 2 ekspresi",
                "color": self.colors.GREEN,
                "emoji": "😊"
            },
            {
                "name": "SEDANG",
                "desc": "20 detik • 4 ekspresi",
                "color": self.colors.YELLOW,
                "emoji": "😐"
            },
            {
                "name": "SULIT",
                "desc": "15 detik • 4 ekspresi • Cepat!",
                "color": self.colors.RED,
                "emoji": "😱"
            }
        ]
        
        y_offset = 220
        for i, diff in enumerate(difficulties):
            self._draw_difficulty_option(screen, diff, i, selected_index, y_offset + (i * 130))
        
        # Instructions
        self._draw_instructions(screen)
    
    def _draw_difficulty_option(self, screen, diff, index, selected_index, y_pos):
        """Draw single difficulty option"""
        is_selected = (index == selected_index)
        
        box_width = 500
        box_height = 100
        box_x = (self.width - box_width) // 2
        
        # Highlight selected
        if is_selected:
            glow_rect = pygame.Rect(box_x - 10, y_pos - 10, box_width + 20, box_height + 20)
            pygame.draw.rect(screen, diff["color"], glow_rect, border_radius=15, width=5)
        
        # Draw box
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (30, 30, 30, 230), box_surface.get_rect(), border_radius=15)
        screen.blit(box_surface, (box_x, y_pos))
        
        # Difficulty name
        name_surface = self.fonts.get_large_font().render(diff["name"], True, diff["color"])
        name_rect = name_surface.get_rect(left=box_x + 30, centery=y_pos + 35)
        screen.blit(name_surface, name_rect)
        
        # Description
        desc_surface = self.fonts.get_small_font().render(diff["desc"], True, self.colors.WHITE)
        desc_rect = desc_surface.get_rect(left=box_x + 30, centery=y_pos + 70)
        screen.blit(desc_surface, desc_rect)
        
        # Emoji
        emoji_surface = self.fonts.get_emoji_font().render(diff["emoji"], True, self.colors.WHITE)
        emoji_rect = emoji_surface.get_rect(right=box_x + box_width - 30, centery=y_pos + 50)
        screen.blit(emoji_surface, emoji_rect)
    
    def _draw_instructions(self, screen):
        """Draw control instructions"""
        inst_y = self.height - 50
        
        text_pilih = " untuk pilih • SPASI untuk mulai • L untuk Leaderboard • ESC untuk keluar"
        text_pilih_surface = self.fonts.get_small_font().render(text_pilih, True, self.colors.GRAY)
        icon_width = 20 if self.icon_up_down else 0
        total_width = icon_width + text_pilih_surface.get_width()
        
        start_x = (self.width - total_width) // 2
        
        if self.icon_up_down:
            screen.blit(self.icon_up_down, (start_x, inst_y))
            start_x += icon_width + 5
        else:
            fallback = self.fonts.get_small_font().render("↑↓", True, self.colors.GRAY)
            screen.blit(fallback, (start_x, inst_y))
            start_x += fallback.get_width()
        
        screen.blit(text_pilih_surface, (start_x, inst_y))


class LeaderboardScreen:
    """Renders leaderboard screen"""
    
    def __init__(self, renderer, colors, fonts, width, height):
        """
        Initialize leaderboard screen
        
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
    
    def draw(self, screen, leaderboard_manager, difficulty="medium"):
        """Draw leaderboard screen"""
        self.renderer.draw_gradient_background(self.colors.DARK_PURPLE, self.colors.BLACK)
        
        # Title
        title = self.fonts.get_title_font().render("LEADERBOARD", True, self.colors.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Difficulty tabs
        self._draw_difficulty_tabs(screen, difficulty)
        
        # Scores table
        scores = leaderboard_manager.get_top_scores(difficulty, 10)
        self._draw_scores_table(screen, scores)
        
        # Instructions
        instructions = "1/2/3 untuk ganti difficulty • ESC untuk kembali"
        inst_surface = self.fonts.get_small_font().render(instructions, True, self.colors.GRAY)
        inst_rect = inst_surface.get_rect(center=(self.width // 2, self.height - 50))
        screen.blit(inst_surface, inst_rect)
    
    def _draw_difficulty_tabs(self, screen, difficulty):
        """Draw difficulty selection tabs"""
        difficulties = ["easy", "medium", "hard"]
        diff_names = {"easy": "MUDAH", "medium": "SEDANG", "hard": "SULIT"}
        diff_colors = {"easy": self.colors.GREEN, "medium": self.colors.YELLOW, "hard": self.colors.RED}
        
        tab_y = 150
        tab_width = 200
        tab_spacing = 220
        start_x = (self.width - (len(difficulties) * tab_spacing - 20)) // 2
        
        for i, diff in enumerate(difficulties):
            tab_x = start_x + (i * tab_spacing)
            is_active = (diff == difficulty)
            
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 50)
            tab_color = diff_colors[diff] if is_active else self.colors.GRAY
            
            if is_active:
                pygame.draw.rect(screen, tab_color, tab_rect, border_radius=10)
                text_color = self.colors.BLACK
            else:
                pygame.draw.rect(screen, tab_color, tab_rect, border_radius=10, width=3)
                text_color = tab_color
            
            tab_text = self.fonts.get_medium_font().render(diff_names[diff], True, text_color)
            tab_text_rect = tab_text.get_rect(center=tab_rect.center)
            screen.blit(tab_text, tab_text_rect)
    
    def _draw_scores_table(self, screen, scores):
        """Draw scores table"""
        table_y = 230
        
        if scores:
            for i, entry in enumerate(scores):
                rank_y = table_y + (i * 45)
                
                # Rank colors
                if i == 0:
                    rank_color = self.colors.YELLOW
                elif i == 1:
                    rank_color = self.colors.LIGHT_BLUE
                elif i == 2:
                    rank_color = self.colors.ORANGE
                else:
                    rank_color = self.colors.WHITE
                
                # Rank
                rank_text = f"#{i + 1}"
                rank_surface = self.fonts.get_medium_font().render(rank_text, True, rank_color)
                screen.blit(rank_surface, (150, rank_y))
                
                # Name
                name_surface = self.fonts.get_medium_font().render(entry["name"], True, self.colors.WHITE)
                screen.blit(name_surface, (250, rank_y))
                
                # Score
                score_text = f"{entry['score']} poin"
                score_surface = self.fonts.get_medium_font().render(score_text, True, self.colors.GREEN)
                screen.blit(score_surface, (550, rank_y))
                
                # Date
                date_surface = self.fonts.get_small_font().render(entry["date"], True, self.colors.GRAY)
                screen.blit(date_surface, (800, rank_y + 5))
        else:
            no_scores = "Belum ada skor tercatat"
            no_scores_surface = self.fonts.get_large_font().render(no_scores, True, self.colors.GRAY)
            no_scores_rect = no_scores_surface.get_rect(center=(self.width // 2, 400))
            screen.blit(no_scores_surface, no_scores_rect)


class NameInputScreen:
    """Renders name input screen"""
    
    def __init__(self, renderer, colors, fonts, width, height):
        """
        Initialize name input screen
        
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
    
    def draw(self, screen, current_name=""):
        """Draw name input screen"""
        self.renderer.draw_gradient_background(self.colors.DARK_PURPLE, self.colors.BLACK)
        
        # Title
        title = self.fonts.get_title_font().render("MASUKKAN NAMA", True, self.colors.YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        
        title_shadow = self.fonts.get_title_font().render("MASUKKAN NAMA", True, (50, 50, 50))
        shadow_rect = title_shadow.get_rect(center=(self.width // 2 + 3, 153))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = "Nama kamu akan muncul di leaderboard!"
        subtitle_surface = self.fonts.get_medium_font().render(subtitle, True, self.colors.LIGHT_BLUE)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 220))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Input box
        self._draw_input_box(screen, current_name)
        
        # Character limit
        self._draw_character_limit(screen, current_name)
        
        # Instructions
        self._draw_instructions(screen)
        
        # Examples
        examples = "Contoh: Player1, Falih, GamerPro"
        example_surface = self.fonts.get_small_font().render(examples, True, self.colors.CYAN)
        example_rect = example_surface.get_rect(center=(self.width // 2, 550))
        screen.blit(example_surface, example_rect)
    
    def _draw_input_box(self, screen, current_name):
        """Draw input box"""
        box_width = 600
        box_height = 80
        box_x = (self.width - box_width) // 2
        box_y = 300
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, self.colors.YELLOW, box_rect, border_radius=15, width=4)
        
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (40, 40, 40, 240), box_surface.get_rect(), border_radius=15)
        screen.blit(box_surface, box_rect)
        
        # Display text
        display_text = current_name if current_name else "Ketik nama kamu..."
        text_color = self.colors.WHITE if current_name else self.colors.GRAY
        name_surface = self.fonts.get_large_font().render(display_text, True, text_color)
        name_rect = name_surface.get_rect(center=(self.width // 2, box_y + 40))
        screen.blit(name_surface, name_rect)
        
        # Blinking cursor
        if current_name and int(pygame.time.get_ticks() / 500) % 2:
            cursor_x = name_rect.right + 10
            cursor_y = box_y + 20
            pygame.draw.rect(screen, self.colors.WHITE, (cursor_x, cursor_y, 3, 40))
    
    def _draw_character_limit(self, screen, current_name):
        """Draw character limit indicator"""
        limit_text = f"{len(current_name)}/15 karakter"
        limit_color = self.colors.RED if len(current_name) >= 15 else self.colors.GRAY
        limit_surface = self.fonts.get_small_font().render(limit_text, True, limit_color)
        limit_rect = limit_surface.get_rect(center=(self.width // 2, 410))
        screen.blit(limit_surface, limit_rect)
    
    def _draw_instructions(self, screen):
        """Draw instructions"""
        instructions = [
            "Ketik nama kamu (A-Z, 0-9, spasi)",
            "ENTER untuk lanjut • BACKSPACE untuk hapus • ESC untuk skip"
        ]
        
        inst_y = 450
        for inst in instructions:
            inst_surface = self.fonts.get_small_font().render(inst, True, self.colors.GRAY)
            inst_rect = inst_surface.get_rect(center=(self.width // 2, inst_y))
            screen.blit(inst_surface, inst_rect)
            inst_y += 35
