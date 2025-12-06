"""
Results Screen - Game results rendering
"""

import math
import pygame


class ResultsScreen:
    """Renders the game results screen"""

    def __init__(self, renderer, colors, fonts, width, height):
        """
        Initialize results screen

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

    def get_button_rects(self):
        """Get button rectangles for mouse click detection"""
        controls_y = 610

        # Play again button at controls_y
        play_rect = pygame.Rect(self.width // 2 - 200, controls_y - 25, 400, 50)

        # Menu button at controls_y + 55
        menu_rect = pygame.Rect(self.width // 2 - 200, controls_y + 55 - 25, 400, 50)

        return [play_rect, menu_rect]

    def draw(self, screen, score, max_score):
        """Draw results screen"""
        self.menu_time += 0.05

        # Animated gradient background
        t = math.sin(self.menu_time * 0.5) * 0.5 + 0.5
        color1 = (int(10 + t * 30), int(5 + t * 20), int(30 + t * 50))
        color2 = (int(40 + t * 40), int(10 + t * 30), int(60 + t * 60))
        self.renderer.draw_gradient_background(color1, color2)

        # Calculate performance
        percentage = (score / max_score * 100) if max_score > 0 else 0
        display_percentage = min(percentage, 100)

        # Determine rank
        rank_info = self._get_rank_info(percentage)

        # Draw decorative circles
        self._draw_decorative_circles(screen, rank_info)

        # Draw title
        self._draw_title(screen, rank_info)

        # Draw rank badge
        self._draw_rank_badge(screen, rank_info)

        # Draw stars
        self._draw_stars(screen, rank_info)

        # Draw results box
        self._draw_results_box(
            screen, rank_info, score, max_score, percentage, display_percentage
        )

        # Draw control instructions
        self._draw_control_instructions(screen)

        # Draw confetti for high scores
        if percentage >= 60:
            self._draw_confetti(screen)

    def _get_rank_info(self, percentage):
        """Get rank information based on percentage"""
        if percentage >= 80:
            return {
                "rank": "S",
                "color": self.colors.YELLOW,
                "message": "LUAR BIASA!",
                "message_color": self.colors.GREEN,
                "particle_color": self.colors.YELLOW,
                "stars": 5,
            }
        elif percentage >= 60:
            return {
                "rank": "A",
                "color": self.colors.GREEN,
                "message": "BAGUS SEKALI!",
                "message_color": self.colors.BLUE,
                "particle_color": self.colors.GREEN,
                "stars": 4,
            }
        elif percentage >= 40:
            return {
                "rank": "B",
                "color": self.colors.BLUE,
                "message": "CUKUP BAIK!",
                "message_color": self.colors.CYAN,
                "particle_color": self.colors.BLUE,
                "stars": 3,
            }
        else:
            return {
                "rank": "C",
                "color": self.colors.GRAY,
                "message": "TERUS BERLATIH!",
                "message_color": self.colors.WHITE,
                "particle_color": self.colors.GRAY,
                "stars": 1,
            }

    def _draw_decorative_circles(self, screen, rank_info):
        """Draw decorative circles with pulse"""
        pulse = math.sin(self.menu_time * 2) * 15
        for i in range(6):
            alpha = int(20 - i * 3)
            size = int(180 + pulse + i * 35)
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                circle_surface, (*rank_info["color"], alpha), (size, size), size, 4
            )
            screen.blit(circle_surface, (self.width // 2 - size, 120 - size))

    def _draw_title(self, screen, rank_info):
        """Draw animated title"""
        bounce = math.sin(self.menu_time * 2.5) * 8
        title_y = 120 + bounce

        # Glow effect
        for i in range(5, 0, -1):
            glow_alpha = 40 - i * 6
            glow_surface = self.fonts.get_title_font().render(
                "SELESAI!", True, (*rank_info["color"], glow_alpha)
            )
            glow_rect = glow_surface.get_rect(center=(self.width // 2, title_y))
            screen.blit(glow_surface, glow_rect)

        title = self.fonts.get_title_font().render("SELESAI!", True, self.colors.WHITE)
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        screen.blit(title, title_rect)

    def _draw_rank_badge(self, screen, rank_info):
        """Draw rank badge with animation"""
        rank_y = 230
        rank_pulse = math.sin(self.menu_time * 3) * 10
        rank_size = 120 + rank_pulse

        # Background circle
        rank_bg_surface = pygame.Surface(
            (rank_size * 2, rank_size * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            rank_bg_surface,
            (*rank_info["color"], 150),
            (rank_size, rank_size),
            rank_size,
        )
        pygame.draw.circle(
            rank_bg_surface,
            (*self.colors.WHITE, 200),
            (rank_size, rank_size),
            rank_size,
            8,
        )
        screen.blit(rank_bg_surface, (self.width // 2 - rank_size, rank_y - rank_size))

        # Rank text
        rank_font = pygame.font.Font(None, 140)
        rank_surface = rank_font.render(rank_info["rank"], True, self.colors.WHITE)
        rank_rect = rank_surface.get_rect(center=(self.width // 2, rank_y))
        screen.blit(rank_surface, rank_rect)

    def _draw_stars(self, screen, rank_info):
        """Draw stars based on performance"""
        star_y = 330
        star_spacing = 60
        total_stars_width = rank_info["stars"] * star_spacing
        star_start_x = (self.width - total_stars_width) // 2 + star_spacing // 2

        for i in range(rank_info["stars"]):
            star_bounce = math.sin(self.menu_time * 2 + i * 0.5) * 5
            star_x = star_start_x + i * star_spacing
            self.renderer.draw_star(
                star_x, star_y + star_bounce, 20, rank_info["particle_color"]
            )

    def _draw_results_box(
        self, screen, rank_info, score, max_score, percentage, display_percentage
    ):
        """Draw results information box"""
        box_y = 390
        box_width = 700
        box_height = 180
        box_rect = pygame.Rect(
            (self.width - box_width) // 2, box_y, box_width, box_height
        )

        # Box glow
        for i in range(5, 0, -1):
            glow_alpha = 40 - i * 6
            glow_surface = pygame.Surface(
                (box_width + i * 8, box_height + i * 8), pygame.SRCALPHA
            )
            pygame.draw.rect(
                glow_surface,
                (*rank_info["color"], glow_alpha),
                glow_surface.get_rect(),
                border_radius=25,
            )
            screen.blit(glow_surface, (box_rect.x - i * 4, box_rect.y - i * 4))

        # Box background
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(
            box_surface, (20, 15, 40, 220), box_surface.get_rect(), border_radius=25
        )
        pygame.draw.rect(
            box_surface,
            rank_info["color"],
            box_surface.get_rect(),
            width=4,
            border_radius=25,
        )
        screen.blit(box_surface, box_rect)

        # Performance message
        self.renderer.draw_text_with_glow(
            rank_info["message"],
            self.fonts.get_large_font(),
            rank_info["message_color"],
            self.width // 2,
            box_y + 35,
        )

        # Score
        score_pulse = math.sin(self.menu_time * 4) * 3
        score_text = f"SKOR: {score} / {max_score}"
        score_font = pygame.font.Font(None, 48)
        score_surface = score_font.render(score_text, True, self.colors.YELLOW)
        score_rect = score_surface.get_rect(
            center=(self.width // 2, box_y + 90 + score_pulse)
        )

        # Score shadow
        shadow_surface = score_font.render(score_text, True, (20, 20, 40))
        shadow_rect = shadow_surface.get_rect(
            center=(self.width // 2 + 3, box_y + 93 + score_pulse)
        )
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(score_surface, score_rect)

        # Percentage bar
        self._draw_percentage_bar(
            screen, box_y, rank_info, percentage, display_percentage
        )

    def _draw_percentage_bar(
        self, screen, box_y, rank_info, percentage, display_percentage
    ):
        """Draw percentage progress bar"""
        bar_y = box_y + 130
        bar_width = 500
        bar_height = 30
        bar_x = (self.width - bar_width) // 2

        # Bar background
        pygame.draw.rect(
            screen,
            (40, 40, 60),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=15,
        )

        # Filled bar
        fill_width = int((display_percentage / 100) * bar_width)
        fill_width = min(fill_width, bar_width)

        if fill_width > 0:
            fill_surface = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)

            # Gradient
            for i in range(fill_width):
                progress = i / bar_width
                bar_color = (
                    int(rank_info["color"][0] * (1 - progress * 0.3)),
                    int(rank_info["color"][1] * (1 - progress * 0.3)),
                    int(rank_info["color"][2] * (1 - progress * 0.3)),
                )
                pygame.draw.line(fill_surface, bar_color, (i, 0), (i, bar_height))

            # Rounded corners mask
            mask_surface = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)
            pygame.draw.rect(
                mask_surface,
                (255, 255, 255, 255),
                (0, 0, fill_width, bar_height),
                border_radius=15,
            )
            fill_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            screen.blit(fill_surface, (bar_x, bar_y))

        # Bar border
        pygame.draw.rect(
            screen,
            self.colors.WHITE,
            (bar_x, bar_y, bar_width, bar_height),
            width=3,
            border_radius=15,
        )

        # Percentage text
        percent_text = f"{int(percentage)}%"
        percent_surface = self.fonts.get_medium_font().render(
            percent_text, True, self.colors.WHITE
        )
        percent_rect = percent_surface.get_rect(
            center=(self.width // 2, bar_y + bar_height // 2)
        )
        screen.blit(percent_surface, percent_rect)

    def _draw_control_instructions(self, screen):
        """Draw control instructions with hover detection"""
        controls_y = 610
        button_pulse = math.sin(self.menu_time * 3) * 8

        mouse_pos = pygame.mouse.get_pos()
        button_rects = self.get_button_rects()

        # Check hover for play again button
        is_play_hovered = button_rects[0].collidepoint(mouse_pos)
        if is_play_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Check hover for menu button
        is_menu_hovered = button_rects[1].collidepoint(mouse_pos)
        if is_menu_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Restart button
        self.renderer.draw_fancy_button(
            "► MAIN LAGI [ENTER]",
            self.width // 2,
            controls_y,
            self.colors.GREEN,
            12 + button_pulse,
            is_hovered=is_play_hovered,
        )

        # Exit button
        self.renderer.draw_fancy_button(
            "◄ MENU [ESC]",
            self.width // 2,
            controls_y + 55,
            self.colors.ORANGE,
            8,
            is_hovered=is_menu_hovered,
        )

    def _draw_confetti(self, screen):
        """Draw confetti particles"""
        for i in range(15):
            x = (self.width // 2) + math.sin(self.menu_time + i) * 400
            y = 100 + ((self.menu_time * 50 + i * 50) % (self.height - 100))
            size = 8 + (i % 3) * 4
            colors = [
                self.colors.YELLOW,
                self.colors.PINK,
                self.colors.CYAN,
                self.colors.GREEN,
                self.colors.ORANGE,
            ]
            color = colors[i % len(colors)]
            rotation = (self.menu_time * 100 + i * 30) % 360

            # Draw rotating rectangle
            rect_surface = pygame.Surface((size * 2, size), pygame.SRCALPHA)
            rect_surface.fill(color)
            rotated = pygame.transform.rotate(rect_surface, rotation)
            rect_rect = rotated.get_rect(center=(int(x), int(y)))
            screen.blit(rotated, rect_rect)
