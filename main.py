"""Contains the whole game for now."""

import arcade
from arcade import Vec2

from grid_view.world_model import WorldModelRec, Structure
from grid_view.custom_sprites import LandTile
from grid_view.utils import world_to_iso, grid_cell_to_world
from grid_view.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE


structure_sprite_list = ["assets/shack.png"]


class GameView(arcade.View):
    """
    View of the world.
    """

    def __init__(self):
        super().__init__()

        self.camera = None
        self.background_color = (59, 107, 88, 255)
        self.buildable_area_sprite = arcade.Sprite("assets/selected_2x2.png")

        self.grid_list = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()
        self.building_sprite_list = arcade.SpriteList()
        self.current_site = None
        self.world_model = WorldModelRec(size=100)
        self.cursor = arcade.SpriteCircle(5, arcade.color.RED)
        self.ui_sprite_list.append(self.cursor)
        for row in self.world_model.idx:
            for entry in row:
                current_coord = grid_cell_to_world(entry)
                pos = world_to_iso(current_coord)
                sprite = LandTile(
                    "assets/grid_cell.png", "assets/selected_grid_cell.png", site=entry
                )
                sprite.position = (pos.x, pos.y)
                self.grid_list.append(sprite)
        self.collided_grid = self.grid_list[0]

    def setup(self):
        """Setup stuff for the level, that isn't in init."""
        self.camera = arcade.Camera2D()
        self.cursor.position = (2 * WINDOW_WIDTH, 2 * WINDOW_HEIGHT)

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
                idx_old = self.collided_grid.un_collide_cursor()
                self.current_site = cursor_grid_collisions[0].collide_cursor()
                idx = self.current_site
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
            self.highlight_buildarea()

    def highlight_buildarea(self):
        """Highlight the area to build."""

        current_cell = self.current_site
        world_location = grid_cell_to_world(current_cell)
        offset = Vec2(16, 16)
        pos = world_to_iso(world_location + offset)
        self.buildable_area_sprite.position = (pos.x, pos.y)
        self.ui_sprite_list.append(self.buildable_area_sprite)

    def update_building_sprites(self):
        """Update building sprites to match the model."""
        self.building_sprite_list = arcade.SpriteList()
        shape = self.world_model.structure_anchor.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                building_id = self.world_model.structure_anchor[i][j]
                if building_id != 0:
                    new_building = arcade.Sprite(structure_sprite_list[building_id - 1])
                    offset = Vec2(new_building.width / 2, new_building.height / 2)
                    world_location = grid_cell_to_world((i, j))  # problem is here
                    pos = world_to_iso(world_location + offset)
                    new_building.position = (pos.x, pos.y)
                    self.building_sprite_list.append(new_building)
        self.building_sprite_list.sort(key=lambda x: x.bottom, reverse=True)

    def build_building(self):
        """Build a building, sync model and view."""
        self.ui_sprite_list.remove(self.buildable_area_sprite)
        shed = Structure(site_size=(2, 2), building_type=1)
        if self.world_model.build_structure(
            site=self.current_site,
            structure=shed,
        ):
            self.update_building_sprites()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.SPACE:
            self.build_building()

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
