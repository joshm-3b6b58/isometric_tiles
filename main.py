"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""

import math
from dataclasses import dataclass

import numpy as np
import arcade
from arcade import Vec2

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Isometric Grid View"
TILE_SIZE = 32


def world_to_iso(coord: Vec2) -> Vec2:
    """Convert world coordinates to view coordinates on the grid."""
    angle_rad = math.radians(30)
    x = coord.x
    y = coord.y

    rotated_x = x * math.cos(-angle_rad) - y * math.sin(-angle_rad)
    rotated_y = x * math.sin(-angle_rad) + y * math.cos(-angle_rad)

    return Vec2(rotated_x, rotated_y)


@dataclass
class SiteModel:
    """Model for the individual grid site"""

    location: Vec2
    selected: bool = False

    def select(self):
        self.selected = True

    def disselect(self):
        self.selected = False


@dataclass
class WorldModel:
    """Model of entities of the world"""

    # numpy array of sites
    def __init__(self, size: int, tile_size: int = TILE_SIZE):
        cols = size
        rows = size
        site_list = [[SiteModel(location=Vec2(i*tile_size,j*tile_size)) for j in range(cols)] for i in range(rows)]
        self.sites = np.array(site_list, dtype=SiteModel)

    def num_sites(self):
        return len(self.sites)


class LandTile(arcade.Sprite):
    """A tile for the ground."""
    def __init__(self, path_or_texture, hilite_path_or_texture):
        super().__init__(path_or_texture)
        self.hilite_path_or_texture = arcade.texture.default_texture_cache.load_or_get_texture(hilite_path_or_texture)

    def change_texture(self):
        self.texture = self.hilite_path_or_texture
    


class GameView(arcade.View):
    """
    View of the world.
    """

    def __init__(self):
        super().__init__()

        self.background_color = (59, 107, 88, 255)
        self.grid_list = arcade.SpriteList()
        for x in range(-100, 100):
            for y in range(-100, 100):
                pos = world_to_iso(Vec2(x * 32, y * 32))
                sprite = LandTile("grid_cell.png","selected_grid_cell.png")
                sprite.position = (pos.x, pos.y)
                self.grid_list.append(sprite)

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.grid_list.draw()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.UP:
            for grid in self.grid_list:
                grid.change_texture()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
