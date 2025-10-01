"""Module for containing the model of the tile based world as a series of numpy arrays."""

from enum import Enum
from dataclasses import dataclass

import numpy as np


class BuildingType(Enum):
    """Types of buildings."""

    SHED = 1
    HOUSE = 2
    FACTORY = 3


@dataclass
class Structure:
    """Model for a structure"""

    building_type: BuildingType
    site_size: tuple[int, int]


class WorldModelRec:
    """Model of sites of the world."""

    def __init__(self, size: int):
        cols = size
        rows = size
        tuple_int_int_dtype = np.dtype([("x", np.int32), ("y", np.int32)])
        self.idx = np.zeros((rows, cols), dtype=(tuple_int_int_dtype))
        self.selected = np.zeros((rows, cols), dtype=bool)
        self.occupied = np.zeros((rows, cols), dtype=bool)
        self.structure_anchor = np.zeros((rows, cols), dtype=np.int16)
        for i in range(rows):
            for j in range(cols):
                self.idx[i, j] = (j, i)

    def check_sites_buildable(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> bool:
        """Check if entire range of sites is buildable."""
        sub_array = self.occupied[start[0] : end[0], start[1] : end[1]]
        print(sub_array)
        if sub_array.any():
            return False
        return True

    def occupy_site(self, site: tuple[int, int]):
        """Set site to occupied."""
        self.occupied[site] = True

    def build_structure(self, structure: Structure, site: tuple[int, int]) -> bool:
        """Build structure at site."""

        start = site
        end = (site[0] + structure.site_size[0], site[1] + structure.site_size[1])
        if self.check_sites_buildable(start, end):
            self.occupied[start[0] : end[0], start[1] : end[1]] = True
            self.structure_anchor[site[0]][site[1]] = structure.building_type
            return True
        return False
