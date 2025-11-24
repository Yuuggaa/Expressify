# UI Architecture Diagram

## Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py (Game)                          │
│                     Uses: ui.UIManager                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ui/ui_manager.py                             │
│                   (Main Orchestrator)                           │
│  • Coordinates all UI components                               │
│  • Manages screen rendering                                    │
│  • Provides unified interface                                  │
└──┬──┬──┬──┬──┬──┬──┬──┬──┬──────────────────────────────────────┘
   │  │  │  │  │  │  │  │  │
   │  │  │  │  │  │  │  │  └─────────────────────┐
   │  │  │  │  │  │  │  │                        │
   ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                        ▼
┌──────────────────────┐ ┌──────────────────────────────────────┐
│   ui/constants.py    │ │        Screen Renderers              │
│  • Colors            │ │  ┌──────────────────────────────┐   │
│  • Dimensions        │ │  │  ui/menu_screen.py           │   │
│  • FontManager       │ │  │  • Main menu rendering       │   │
└──────────────────────┘ │  └──────────────────────────────┘   │
                         │  ┌──────────────────────────────┐   │
┌──────────────────────┐ │  │  ui/game_screen.py           │   │
│ ui/base_renderer.py  │ │  │  • Game screen rendering     │   │
│  • Gradient BG       │ │  │  • Camera feed display       │   │
│  • Text effects      │ │  └──────────────────────────────┘   │
│  • Buttons           │ │  ┌──────────────────────────────┐   │
│  • Stars             │ │  │  ui/results_screen.py        │   │
└──────────────────────┘ │  │  • Results rendering         │   │
                         │  │  • Rank badges               │   │
┌──────────────────────┐ │  └──────────────────────────────┘   │
│  ui/animations.py    │ │  ┌──────────────────────────────┐   │
│  • ParticleSystem    │ │  │  ui/other_screens.py         │   │
│  • FloatingImages    │ │  │  • DifficultyScreen          │   │
│  • ConfettiSystem    │ │  │  • LeaderboardScreen         │   │
└──────────────────────┘ │  │  • NameInputScreen           │   │
                         │  └──────────────────────────────┘   │
┌──────────────────────┐ └──────────────────────────────────────┘
│ ui/image_manager.py  │
│  • Load images       │
│  • Render animations │
│  • Image caching     │
└──────────────────────┘
```

## Component Relationships

```
UIManager
    ├── Uses: Colors (constants.py)
    ├── Uses: Dimensions (constants.py)
    ├── Uses: FontManager (constants.py)
    ├── Uses: UIRenderer (base_renderer.py)
    ├── Uses: ParticleSystem (animations.py)
    ├── Uses: FloatingImageSystem (animations.py)
    ├── Uses: ConfettiSystem (animations.py)
    ├── Uses: ImageManager (image_manager.py)
    ├── Uses: MenuScreen (menu_screen.py)
    ├── Uses: GameScreen (game_screen.py)
    ├── Uses: ResultsScreen (results_screen.py)
    ├── Uses: DifficultyScreen (other_screens.py)
    ├── Uses: LeaderboardScreen (other_screens.py)
    └── Uses: NameInputScreen (other_screens.py)

Screen Renderers (All)
    ├── Uses: UIRenderer
    ├── Uses: Colors
    ├── Uses: FontManager
    └── Uses: Dimensions (some)

Animation Systems
    ├── ParticleSystem → Uses: Colors
    ├── FloatingImageSystem → Uses: ImageManager
    └── ConfettiSystem → Uses: Colors

UIRenderer
    ├── Uses: Colors
    └── Uses: FontManager
```

## Data Flow

```
1. Game Loop (main.py)
        ↓
2. UIManager Method Call
   (e.g., draw_menu, draw_game)
        ↓
3. Screen Renderer
   (e.g., MenuScreen.draw())
        ↓
4. Uses Base Utilities
   - UIRenderer methods
   - Animation systems
   - Image manager
        ↓
5. Pygame Rendering
   - Surfaces created
   - Blitted to screen
```

## Example: Drawing Menu Screen

```
main.py
  └─→ ui_manager.draw_menu(selected_index)
       └─→ menu_screen.draw(screen, selected_index)
            ├─→ renderer.draw_gradient_background()
            ├─→ renderer.draw_text_with_glow()
            ├─→ renderer.draw_star()
            └─→ screen.blit()
       └─→ particle_system.update_and_draw(screen)
       └─→ floating_image_system.update_and_draw(screen, images)
```

## Example: Drawing Game Screen

```
main.py
  └─→ ui_manager.draw_game_with_debug(...)
       └─→ game_screen.draw_with_debug(...)
            ├─→ renderer.draw_gradient_background()
            ├─→ _draw_camera_feed()
            ├─→ image_manager.draw_animated_expression_image()
            ├─→ _draw_challenge_header()
            ├─→ _draw_score_panel()
            └─→ _draw_timer_panel()
       └─→ particle_system.update_and_draw(screen)
       └─→ floating_image_system.update_and_draw(screen, images)
```

## Module Responsibilities

| Module                | Primary Responsibility | Secondary Functions        |
| --------------------- | ---------------------- | -------------------------- |
| **ui_manager.py**     | Orchestrate all UI     | Initialize subsystems      |
| **constants.py**      | Configuration          | Font management            |
| **base_renderer.py**  | Common utilities       | Text effects, shapes       |
| **animations.py**     | Visual effects         | Particles, floating images |
| **image_manager.py**  | Asset loading          | Image rendering            |
| **menu_screen.py**    | Menu rendering         | Menu logic                 |
| **game_screen.py**    | Game rendering         | Camera display             |
| **results_screen.py** | Results display        | Rank calculation           |
| **other_screens.py**  | Misc screens           | Input handling             |

## Communication Patterns

### Initialization Phase

```
main.py creates UIManager
    → UIManager creates all subsystems
        → Each subsystem initializes its resources
            → Resources cached for reuse
```

### Rendering Phase

```
main.py calls ui_manager.draw_X()
    → ui_manager delegates to appropriate screen
        → screen uses renderer utilities
            → renderer uses constants and fonts
                → pygame renders to display
```

### Update Phase

```
Animation systems update state each frame
    → Position calculations
    → Rotation updates
    → Alpha adjustments
        → Render with updated values
```

## Design Principles Applied

1. **Single Responsibility**: Each module has one job
2. **Open/Closed**: Open for extension, closed for modification
3. **Dependency Inversion**: Depend on abstractions
4. **Composition over Inheritance**: Build with components
5. **DRY**: Don't Repeat Yourself (shared utilities)
6. **KISS**: Keep It Simple, Stupid (focused modules)

## Benefits Visualization

```
Before:                          After:
┌─────────────────┐             ┌──────────────┐
│                 │             │ UIManager    │
│   ui_manager    │             │ (Orchestrator)│
│   (650 lines)   │    ══►      └──────┬───────┘
│                 │                    │
│  Everything!    │              ┌─────┴─────┐
│                 │              │ 9 Modules │
└─────────────────┘              └───────────┘
                                Each 70-300 lines
  Monolithic                     Modular & Clean
  Hard to maintain               Easy to maintain
  Difficult to test              Easy to test
  Low cohesion                   High cohesion
  High coupling                  Low coupling
```
