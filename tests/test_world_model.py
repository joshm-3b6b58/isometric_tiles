"""Tests for the world model."""

from numpy.testing import assert_array_equal
import numpy as np

from grid_view.world_model import WorldModelRec, BuildingModel


def test_world_model_rec():
    wm = WorldModelRec(size=3)
    test_array_false = np.array(
        [[False, False, False], [False, False, False], [False, False, False]]
    )
    tuple_int_int_dtype = np.dtype([("x", np.int32), ("y", np.int32)])

    test_array_idx = np.array(
        [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
        ],
        dtype=tuple_int_int_dtype,
    )

    print(wm.idx[0][0])
    assert_array_equal(wm.selected, test_array_false)
    assert_array_equal(wm.occupied, test_array_false)
    assert_array_equal(wm.idx, test_array_idx)

    assert wm.check_sites_buildable((0, 0), (2, 2)) is True

    wm.occupy_site((0, 0))

    test_array_00_true = np.array(
        [[True, False, False], [False, False, False], [False, False, False]]
    )
    assert_array_equal(wm.occupied, test_array_00_true)
    assert wm.check_sites_buildable((0, 0), (2, 2)) is False

    test_structure = BuildingModel(building_type=2, footprint=(2, 2))
    assert wm.build_structure(site=(1, 1), structure=test_structure) is True
    test_array_built = np.array(
        [[True, False, False], [False, True, True], [False, True, True]]
    )
    test_array_anchor = np.array(
        [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
    )  # Only the anchor point has building_type=1

    assert_array_equal(wm.structure_anchor, test_array_anchor)
    assert_array_equal(wm.occupied, test_array_built)
    assert wm.build_structure(site=(1, 1), structure=test_structure) is False
