# Isometric Grid View

Isometric Grid View is a Python application for visualizing and interacting with a tile-based world using isometric projection. Built with [arcade](https://api.arcade.academy/en/latest/) and [numpy](https://numpy.org/), it supports grid navigation, site selection, and building placement.

## Features

- Isometric rendering of a grid world
- Customizable tile sprites
- Keyboard navigation and site selection
- Building placement with collision detection
- Modular code structure for easy extension
- Unit tests for core functionality

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd grid-view
   ```

2. **Install dependencies:**
   ```sh
   uv sync --locked --all-extras --dev
   ```

## Usage

Run the main application:

```sh
uv run python main.py
```

Use arrow keys to move the cursor. Press `SPACE` to build a structure at the selected site.

## Project Structure

- `main.py`: Main game loop and view logic
- `grid_view/`: Core modules
  - `constants.py`: App constants
  - `custom_sprites.py`: Custom sprite classes ([`LandTile`](grid_view/custom_sprites.py))
  - `utils.py`: Helper functions ([`world_to_iso`](grid_view/utils.py), [`grid_cell_to_world`](grid_view/utils.py))
  - `world_model.py`: World model and building logic ([`WorldModelRec`](grid_view/world_model.py), [`Structure`](grid_view/world_model.py))
- `assets/`: Sprite and image assets
- `tests/`: Unit tests

## Testing

Run all tests with:

```sh
uv run pytest tests
```

## License

MIT License

## Contributing

Pull requests and issues are welcome!