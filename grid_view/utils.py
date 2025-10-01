"""Helper funtions for grid view."""
from arcade import Vec2
import numpy as np

from grid_view.constants import TILE_SIZE


def world_to_iso(coord: Vec2) -> Vec2:
    """Convert world coordinates to view coordinates on the grid."""
    x = coord.x
    y = coord.y

    rotated_x = (x - y) * np.sqrt(3) / 2
    rotated_y = (x + y) / 2
    return Vec2(rotated_x, rotated_y)


def grid_cell_to_world(cell: tuple[int, int], tile_size=TILE_SIZE) -> Vec2:
    """Convert grid cell to world coordinates."""
    return Vec2(cell[0] * tile_size, cell[1] * tile_size)
