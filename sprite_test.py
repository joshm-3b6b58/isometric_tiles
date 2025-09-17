from main import LandTile
import arcade  

def test_land_tile():
    """Test that the land tile functionality."""
    dt_path = "grid_cell.png"
    ht_path = "selected_grid_cell.png"
    sprite = LandTile(dt_path, ht_path)
    default_texture = arcade.texture.default_texture_cache.load_or_get_texture(dt_path)
    hilite_texture =  arcade.texture.default_texture_cache.load_or_get_texture(ht_path)
    assert sprite.texture == default_texture
    sprite.change_texture()
    assert sprite.texture == hilite_texture