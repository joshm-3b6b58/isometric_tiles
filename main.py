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
TILE_SIZE = 35


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
        """Set this site as selected."""
        self.selected = True

    def disselect(self):
        """Set this site as not selected."""
        self.selected = False


@dataclass
class WorldModel:
    """Model of sites of the world."""

    # numpy array of sites
    def __init__(self, size: int, tile_size: int = TILE_SIZE):
        cols = size
        rows = size
        site_list = [
            [
                SiteModel(location=Vec2(i * tile_size, j * tile_size))
                for j in range(cols)
            ]
            for i in range(rows)
        ]
        self.sites = np.array(site_list, dtype=SiteModel)


class LandTile(arcade.Sprite):
    """A tile for the ground."""

    def __init__(self, path_or_texture, hilite_path_or_texture, site: tuple[int, int]):
        super().__init__(path_or_texture)
        self.hilite_path_or_texture = (
            arcade.texture.default_texture_cache.load_or_get_texture(
                hilite_path_or_texture
            )
        )
        self.default_texture = self.texture
        self.site = site

    def collide_cursor(self):
        """Change the texture to the highligthed tile.

        Returns the address of the site."""
        self.texture = self.hilite_path_or_texture
        return self.site

    def un_collide_cursor(self):
        """Change the texture to the default tile.

        Returns the address of the site."""
        self.texture = self.default_texture
        return self.site


class GameView(arcade.View):
    """
    View of the world.
    """

    def __init__(self):
        super().__init__()

        self.camera = None
        self.background_color = (59, 107, 88, 255)
        self.grid_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.world_model = WorldModel(size=100)
        self.cursor = arcade.SpriteCircle(5, arcade.color.RED)
        self.cursor.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.foreground_list.append(self.cursor)
        for x_idx, x in enumerate(self.world_model.sites):
            for y_idx, site in enumerate(x):
                pos = world_to_iso(site.location)
                sprite = LandTile(
                    "grid_cell.png", "selected_grid_cell.png", site=(x_idx, y_idx)
                )
                sprite.position = (pos.x, pos.y)
                self.grid_list.append(sprite)
        self.collided_grid = self.grid_list[0]

    def setup(self):
        """Setup stuff for the level, that isn't in init."""
        self.camera = arcade.Camera2D()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.camera.use()

        self.grid_list.draw()
        self.foreground_list.draw()

    def on_update(self, delta_time):
        """
        Handle update logic.
        """

        cursor_grid_collisions = arcade.check_for_collision_with_list(
            self.cursor, self.grid_list
        ) # Some kind of off by one collision to debug.
        self.camera.position = self.cursor.position
        if cursor_grid_collisions:
            if self.collided_grid is not cursor_grid_collisions[0]:
                idx_old = self.collided_grid.un_collide_cursor()
                self.world_model.sites[idx_old[0]][idx_old[1]].disselect()
                idx = cursor_grid_collisions[0].collide_cursor()
                self.world_model.sites[idx[0]][idx[1]].select()
                self.collided_grid = cursor_grid_collisions[0]

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        if key == arcade.key.UP:
            self.cursor.center_y += 10
        elif key == arcade.key.DOWN:
            self.cursor.center_y -= 10
        elif key == arcade.key.LEFT:
            self.cursor.center_x -= 10
        elif key == arcade.key.RIGHT:
            self.cursor.center_x += 10

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
    game.setup()
    # Show GameView on screen
    window.show_view(game)


    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
