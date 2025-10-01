"""Test for custome sprites."""

import arcade

from grid_view.custom_sprites import LandTile


def test_land_tile():
    """Test that the land tile functionality."""
    dt_path = "assets/grid_cell.png"
    ht_path = "assets/selected_grid_cell.png"
    site = (20, 31)
    sprite = LandTile(dt_path, ht_path, site)
    default_texture = arcade.texture.default_texture_cache.load_or_get_texture(dt_path)
    hilite_texture = arcade.texture.default_texture_cache.load_or_get_texture(ht_path)
    assert sprite.texture == default_texture
    assert sprite.collide_cursor() == site
    assert sprite.texture == hilite_texture
    assert sprite.un_collide_cursor() == site
    assert sprite.texture == default_texture
