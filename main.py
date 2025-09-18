"""Contains the whole game for now."""

from dataclasses import dataclass

import numpy as np
import arcade
from arcade import Vec2

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Isometric Grid View"
TILE_SIZE = 40


def world_to_iso(coord: Vec2) -> Vec2:
    """Convert world coordinates to view coordinates on the grid."""
    x = coord.x
    y = coord.y

    rotated_x = (x - y) * np.sqrt(3) / 2
    rotated_y = (x + y) / 2
    return Vec2(rotated_x, rotated_y)


@dataclass
class Structure:
    """Model for a structure"""

    site_size: tuple[int, int]


@dataclass
class SiteModel:
    """Model for the individual grid site"""

    location: Vec2
    index: tuple[int, int]
    structure_anchor: Structure = None
    selected: bool = False
    occupied: bool = False

    def select(self):
        """Set this site as selected."""
        self.selected = True

    def disselect(self):
        """Set this site as not selected."""
        self.selected = False

    def add_structure(self, structure):
        """Add the ancor point of a structure."""
        self.structure_anchor = structure

    def occupy_site(self):
        """Set site to occupied."""
        self.occupied = True

    def free_site(self):
        """Free up site."""
        self.occupied = False


@dataclass
class WorldModel:
    """Model of sites of the world."""

    def __init__(self, size: int, tile_size: int = TILE_SIZE):
        cols = size
        rows = size
        site_list = [
            [
                SiteModel(location=Vec2(i * tile_size, j * tile_size), index=(i, j))
                for j in range(cols)
            ]
            for i in range(rows)
        ]
        self.sites = np.array(site_list, dtype=SiteModel)

    def check_sites_buildable(self, xrange: tuple[int, int], yrange: tuple[int, int]):
        """Check if entire range of sites is buildable."""
        print(f"Checking buildable for x:{xrange} y:{yrange}")
        for site_x in range(*xrange):
            for site_y in range(*yrange):
                if self.sites[site_x, site_y].occupied is True:
                    print(f"Site at {site_x},{site_y} is occupied, giving up")
                    return False
        print("site buildable")
        return True

    def build_structure(self, structure: Structure, site: tuple[int, int]):
        """Allocate a structure to grid sites in the world.

        Returns a true if site is built on, returns false if not.
        """
        start_x = site[0] - structure.site_size[0] + 1
        end_x = site[0] + 1
        start_y = site[1] - structure.site_size[1] + 1
        end_y = site[1] + 1
        print(f"x range: {start_x},{end_x} y range: {start_y}, {end_y}")
        if self.check_sites_buildable((start_x, end_x), (start_y, end_y)):
            print(f"Should be false: {self.sites[start_x][start_y].occupied}")
            for site_x in range(start_x, end_x):
                for site_y in range(start_y, end_y):
                    if self.sites[site_x, site_y].occupied is False:
                        print(f"occupying site ({site_x},{site_y})")
                        self.sites[site_x, site_y].occupy_site()
        else:
            return False

        self.sites[site[0]][site[1]].add_structure(structure)
        print(f"should be True: {self.sites[start_x][start_y].occupied}")
        return True


class BuildAreaOverlay(arcade.SpriteSolidColor):
    """A transparent overlay to show the build area."""


class LandTile(arcade.Sprite):
    """A tile for the ground."""

    def __init__(self, path_or_texture, hilite_path_or_texture, site: SiteModel):
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
        self.ui_sprite_list = arcade.SpriteList()
        self.building_sprite_list = arcade.SpriteList()
        self.current_site = None
        self.world_model = WorldModel(size=100)
        self.cursor = arcade.SpriteCircle(5, arcade.color.RED)
        self.ui_sprite_list.append(self.cursor)
        for x in self.world_model.sites:
            for site in x:
                pos = world_to_iso(site.location)
                sprite = LandTile("grid_cell.png", "selected_grid_cell.png", site=site)
                sprite.position = (pos.x, pos.y)
                self.grid_list.append(sprite)
        self.collided_grid = self.grid_list[0]

    def setup(self):
        """Setup stuff for the level, that isn't in init."""
        self.camera = arcade.Camera2D()
        self.cursor.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

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
        self.ui_sprite_list.draw()
        self.building_sprite_list.draw()

    def on_update(self, delta_time):
        """
        Handle update logic.
        """

        cursor_grid_collisions = arcade.check_for_collision_with_list(
            self.cursor, self.grid_list
        )
        self.camera.position = self.cursor.position
        if cursor_grid_collisions:
            if self.collided_grid is not cursor_grid_collisions[0]:
                idx_old = self.collided_grid.un_collide_cursor().index
                self.world_model.sites[idx_old[0]][idx_old[1]].disselect()
                self.current_site = cursor_grid_collisions[0].collide_cursor()
                idx = self.current_site.index
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
        elif key == arcade.key.SPACE:
            self.build_building()

    def build_building(self):
        """Build a building, sync model and view."""
        shed = Structure(site_size=(2, 2))
        print(self.current_site)
        if self.world_model.build_structure(
            structure=shed, site=self.current_site.index
        ):
            new_building = arcade.Sprite("shack.png")
            offset = Vec2(new_building.width / 2, new_building.height / 2)
            pos = world_to_iso(self.current_site.location + offset)
            new_building.position = (pos.x, pos.y)
            self.building_sprite_list.append(new_building)
        else:
            print("Site occupied, can't build.")

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
