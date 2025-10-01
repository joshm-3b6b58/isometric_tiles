"""Custom sprites for the grid view."""

import arcade


class BuildAreaOverlay(arcade.SpriteSolidColor):
    """A transparent overlay to show the build area."""


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
