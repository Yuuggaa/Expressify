# UI Module - Modular UI Architecture

## Overview

The UI module has been refactored from a monolithic `ui_manager.py` file into a clean, modular package structure. This improves code organization, maintainability, and scalability.

## Structure

```
src/ui/
├── __init__.py              # Package exports
├── ui_manager.py            # Main orchestrator class
├── constants.py             # Colors, dimensions, font management
├── base_renderer.py         # Base rendering utilities
├── animations.py            # Particle and animation systems
├── image_manager.py         # Expression image loading and rendering
├── menu_screen.py           # Main menu screen renderer
├── game_screen.py           # Game playing screen renderer
├── results_screen.py        # Results screen renderer
└── other_screens.py         # Difficulty, leaderboard, name input screens
```

## Components

### 1. **constants.py**

- `Colors`: Color palette constants
- `Dimensions`: UI dimension constants
- `FontManager`: Font loading and management

### 2. **base_renderer.py**

- `UIRenderer`: Base rendering utilities
  - Gradient backgrounds
  - Text with shadow/glow effects
  - Fancy buttons
  - Stars and decorative elements
  - HSV to RGB color conversion

### 3. **animations.py**

- `Particle`: Single particle representation
- `ParticleSystem`: Background floating particles
- `FloatingImage`: Single floating expression image
- `FloatingImageSystem`: Manages multiple floating images
- `ConfettiSystem`: Celebration confetti animation

### 4. **image_manager.py**

- `ImageManager`: Expression image management
  - Loads expression photos from assets
  - Renders animated expression images with swaying/bobbing effects
  - Manages image cache

### 5. **menu_screen.py**

- `MenuScreen`: Main menu rendering
  - Animated rainbow title
  - Menu options with hover effects
  - Instructions box
  - Team information
  - Navigation controls

### 6. **game_screen.py**

- `GameScreen`: Game screen rendering
  - Camera feed with border effects
  - Challenge header with emoji support
  - Score and timer panels
  - Debug mode with animated expression images

### 7. **results_screen.py**

- `ResultsScreen`: Results screen rendering
  - Rank badges (S, A, B, C)
  - Star ratings
  - Score display with animations
  - Percentage progress bar
  - Confetti for high scores

### 8. **other_screens.py**

- `DifficultyScreen`: Difficulty selection
- `LeaderboardScreen`: Leaderboard display
- `NameInputScreen`: Player name input

### 9. **ui_manager.py**

- `UIManager`: Main orchestrator
  - Initializes all subsystems
  - Coordinates screen rendering
  - Manages animation systems
  - Provides unified interface for game logic

## Usage

```python
from ui import UIManager

# Initialize
ui_manager = UIManager(width=1280, height=720)

# Draw different screens
ui_manager.draw_menu(selected_index=0)
ui_manager.draw_game(frame, challenge, score, time)
ui_manager.draw_results(score, max_score)
ui_manager.draw_difficulty_selection(selected_index=1)
ui_manager.draw_leaderboard(leaderboard_manager, difficulty="medium")
ui_manager.draw_name_input(current_name="Player")
```

## Benefits of Modular Architecture

### 1. **Separation of Concerns**

Each module has a single, well-defined responsibility:

- Constants manage configuration
- Animations handle visual effects
- Screens handle specific UI states
- Image manager handles image resources

### 2. **Maintainability**

- Easier to locate and fix bugs
- Changes to one screen don't affect others
- Clear module boundaries

### 3. **Testability**

- Each component can be tested independently
- Mock dependencies easily
- Unit test individual screens

### 4. **Scalability**

- Easy to add new screens
- Simple to extend animation systems
- New UI elements can be added without touching existing code

### 5. **Readability**

- Smaller, focused files
- Clear naming conventions
- Well-documented components

### 6. **Reusability**

- Base renderer utilities can be used across screens
- Animation systems are reusable
- Image manager can be extended for new image types

## Design Patterns Used

### 1. **Composition over Inheritance**

`UIManager` composes various specialized components rather than inheriting behavior.

### 2. **Single Responsibility Principle**

Each class has one primary responsibility.

### 3. **Dependency Injection**

Components receive their dependencies through constructors.

### 4. **Facade Pattern**

`UIManager` provides a simplified interface to the complex subsystem.

## Migration from Old Code

The refactoring maintained 100% backward compatibility with the game logic. All existing methods are preserved:

- `draw_menu()`
- `draw_game()`
- `draw_game_with_debug()`
- `draw_results()`
- `draw_difficulty_selection()`
- `draw_leaderboard()`
- `draw_name_input()`

## Future Enhancements

Potential areas for further improvement:

1. **Configuration System**: Move more constants to external config files
2. **Theme System**: Support multiple color themes
3. **Animation Presets**: Predefined animation configurations
4. **Screen Transitions**: Smooth transitions between screens
5. **Responsive Design**: Better handling of different screen sizes
6. **Asset Management**: Centralized asset loading and caching

## Performance Considerations

- **Image Caching**: Expression images loaded once at startup
- **Font Caching**: Fonts initialized once and reused
- **Surface Reuse**: Alpha surfaces created per frame but optimized
- **Particle Count**: Limited to reasonable numbers (30-40 particles)

## Contributing

When adding new UI components:

1. Follow the existing module structure
2. Use composition over inheritance
3. Document all public methods
4. Keep methods focused and small
5. Use type hints where appropriate
6. Follow the existing naming conventions

## Credits

**Refactored by**: AI Assistant
**Original Design by**: Tim Pengembang Expressify

- Falih Dzakwan Zuhdi
- Hamka Putra Andiyan
- Bayu Ega Ferdana
