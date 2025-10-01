"""Test for helper functions."""

from pytest import approx
from arcade import Vec2

from grid_view.utils import world_to_iso, grid_cell_to_world


def test_world_to_iso():
    """Test that the isometric conversions are correct for a unit square."""
    assert world_to_iso(Vec2(0, 0)).x == 0
    assert world_to_iso(Vec2(0, 0)).y == 0
    assert world_to_iso(Vec2(1, 0)).x == approx(0.866, rel=1e-3)
    assert world_to_iso(Vec2(1, 0)).y == approx(0.5, rel=1e-3)
    assert world_to_iso(Vec2(0, 1)).x == approx(-0.866, rel=1e-3)
    assert world_to_iso(Vec2(0, 1)).y == approx(0.5, rel=1e-3)
    assert world_to_iso(Vec2(1, 1)).x == approx(0, rel=1e-3)
    assert world_to_iso(Vec2(1, 1)).y == approx(1, rel=1e-3)


def test_grid_cell_to_world():
    """Test that the grid cell to world conversion is correct."""
    assert grid_cell_to_world((0, 0), tile_size=11) == Vec2(0, 0)
    assert grid_cell_to_world((1, 0), tile_size=11) == Vec2(11, 0)
    assert grid_cell_to_world((0, 1), tile_size=11) == Vec2(0, 11)
    assert grid_cell_to_world((2, 2), tile_size=11) == Vec2(22, 22)
