"""
UI Manager - Main orchestrator for all UI components
"""

import pygame
from .constants import Colors, Dimensions, FontManager
from .base_renderer import UIRenderer
from .animations import ParticleSystem, FloatingImageSystem, ConfettiSystem
from .image_manager import ImageManager
from .menu_screen import MenuScreen
from .game_screen import GameScreen
from .results_screen import ResultsScreen
from .other_screens import DifficultyScreen, LeaderboardScreen, NameInputScreen


class UIManager:
    """
    Main UI Manager that coordinates all UI components

    This class serves as the central point for rendering all UI screens
    in the Expressify game. It manages:
    - Color and font configuration
    - Particle and animation systems
    - Expression image loading
    - Screen-specific rendering (menu, game, results, etc.)
    """

    def __init__(self, width, height):
        """
        Initialize UI manager

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.width = width
        self.height = height
        self.screen = (
            pygame.display.get_surface()
        )  # Get existing surface instead of creating new

        # Initialize core components
        self.colors = Colors()
        self.dimensions = Dimensions()
        self.fonts = FontManager()

        # Initialize renderer
        self.renderer = UIRenderer(self.screen, self.colors, self.fonts)

        # Initialize animation systems
        self.particle_system = ParticleSystem(width, height, self.colors)
        self.floating_image_system = FloatingImageSystem(width, height)
        self.confetti_system = ConfettiSystem(width, height, self.colors)

        # Initialize image manager
        self.image_manager = ImageManager(self.dimensions.IMAGE_SIZE)

        # Initialize screen renderers
        self.menu_screen = MenuScreen(
            self.renderer, self.colors, self.fonts, width, height
        )
        self.game_screen = GameScreen(
            self.renderer, self.colors, self.fonts, width, height, self.dimensions
        )
        self.results_screen = ResultsScreen(
            self.renderer, self.colors, self.fonts, width, height
        )
        self.difficulty_screen = DifficultyScreen(
            self.renderer, self.colors, self.fonts, width, height
        )
        self.leaderboard_screen = LeaderboardScreen(
            self.renderer, self.colors, self.fonts, width, height
        )
        self.name_input_screen = NameInputScreen(
            self.renderer, self.colors, self.fonts, width, height
        )

    def draw_menu(self, selected_index=0):
        """
        Draw main menu screen

        Args:
            selected_index: Index of currently selected menu option
        """
        self.menu_screen.draw(self.screen, selected_index)
        self.particle_system.update_and_draw(self.screen)
        self.floating_image_system.update_and_draw(
            self.screen, self.image_manager.get_expression_images()
        )

    def draw_game(self, frame, current_challenge, score, remaining_time):
        """
        Draw game playing screen

        Args:
            frame: Camera frame from OpenCV
            current_challenge: Current expression challenge key
            score: Current player score
            remaining_time: Remaining time in seconds
        """
        self.game_screen.draw(
            self.screen, frame, current_challenge, score, remaining_time
        )
        # Pass camera area to avoid particles and floating images overlapping the camera feed
        camera_area = self.game_screen.get_camera_area()
        self.particle_system.update_and_draw(self.screen, exclude_area=camera_area)
        self.floating_image_system.update_and_draw(
            self.screen,
            self.image_manager.get_expression_images(),
            exclude_area=camera_area,
        )

    def draw_game_with_debug(
        self, frame, current_challenge, score, remaining_time, detected_expression
    ):
        """
        Draw game screen with debug information

        Args:
            frame: Camera frame from OpenCV
            current_challenge: Current expression challenge key
            score: Current player score
            remaining_time: Remaining time in seconds
            detected_expression: Currently detected expression
        """
        self.game_screen.draw_with_debug(
            self.screen,
            frame,
            current_challenge,
            score,
            remaining_time,
            detected_expression,
            self.image_manager,
        )
        # Pass camera area to avoid particles and floating images overlapping the camera feed
        camera_area = self.game_screen.get_camera_area()
        self.particle_system.update_and_draw(self.screen, exclude_area=camera_area)
        self.floating_image_system.update_and_draw(
            self.screen,
            self.image_manager.get_expression_images(),
            exclude_area=camera_area,
        )

    def draw_results(self, score, max_score):
        """
        Draw game results screen

        Args:
            score: Final player score
            max_score: Maximum possible score
        """
        self.results_screen.draw(self.screen, score, max_score)
        self.particle_system.update_and_draw(self.screen)

    def draw_difficulty_selection(self, selected_index=0):
        """
        Draw difficulty selection screen

        Args:
            selected_index: Index of currently selected difficulty
        """
        self.difficulty_screen.draw(self.screen, selected_index)
        self.particle_system.update_and_draw(self.screen)

    def draw_leaderboard(self, leaderboard_manager, difficulty="medium"):
        """
        Draw leaderboard screen

        Args:
            leaderboard_manager: LeaderboardManager instance
            difficulty: Current difficulty filter ("easy", "medium", "hard")
        """
        self.leaderboard_screen.draw(self.screen, leaderboard_manager, difficulty)
        self.particle_system.update_and_draw(self.screen)

    def draw_name_input(self, current_name=""):
        """
        Draw name input screen

        Args:
            current_name: Currently entered name
        """
        self.name_input_screen.draw(self.screen, current_name)
        self.particle_system.update_and_draw(self.screen)
