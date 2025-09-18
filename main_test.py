import numpy as np
from numpy.testing import assert_array_equal


from main import world_to_iso, WorldModel, SiteModel, Structure
from pytest import approx
from arcade import Vec2

# fix this later
# def test_world_to_iso():
#     """Test that the isometric conversions are correct for a unit square."""
#     assert world_to_iso(Vec2(0, 0)).x == 0
#     assert world_to_iso(Vec2(0, 0)).y == 0
#     assert world_to_iso(Vec2(1, 0)).x == approx(0.866, rel=1e-3)
#     assert world_to_iso(Vec2(1, 0)).y == approx(-0.5, rel=1e-3)
#     assert world_to_iso(Vec2(0, 1)).x == approx(0.5, rel=1e-3)
#     assert world_to_iso(Vec2(0, 1)).y == approx(0.866, rel=1e-3)
#     assert world_to_iso(Vec2(1, 1)).x == approx(0.5 + 0.866, rel=1e-3)
#     assert world_to_iso(Vec2(1, 1)).y == approx(0.866 - 0.5, rel=1e-3)


def test_site_model():
    """Test the model for an individual site."""
    site = SiteModel(location=Vec2(0, 0), index=(0, 0), selected=False)

    assert site.selected is False
    site.disselect()
    assert site.selected is False
    site.select()
    assert site.selected is True
    site.disselect()
    assert site.selected is False


def test_world_model():
    """Test the array representation of the world model."""
    wm = WorldModel(size=4, tile_size=1)
    assert len(wm.sites) == 4
    compare_array = [
        [
            SiteModel(Vec2(0, 0), index=(0, 0)),
            SiteModel(Vec2(0, 1), index=(0, 1)),
            SiteModel(Vec2(0, 2), index=(0, 2)),
            SiteModel(Vec2(0, 3), index=(0, 3)),
        ],
        [
            SiteModel(Vec2(1, 0), index=(1, 0)),
            SiteModel(Vec2(1, 1), index=(1, 1)),
            SiteModel(Vec2(1, 2), index=(1, 2)),
            SiteModel(Vec2(1, 3), index=(1, 3)),
        ],
        [
            SiteModel(Vec2(2, 0), index=(2, 0)),
            SiteModel(Vec2(2, 1), index=(2, 1)),
            SiteModel(Vec2(2, 2), index=(2, 2)),
            SiteModel(Vec2(2, 3), index=(2, 3)),
        ],
        [
            SiteModel(Vec2(3, 0), index=(3, 0)),
            SiteModel(Vec2(3, 1), index=(3, 1)),
            SiteModel(Vec2(3, 2), index=(3, 2)),
            SiteModel(Vec2(3, 3), index=(3, 3)),
        ],
    ]
    assert_array_equal(wm.sites, compare_array)
    assert wm.sites[0][0].selected is False
    wm.sites[0][0].select()
    assert wm.sites[0][0].selected is True
    assert wm.sites[2][2].occupied is False
    wm.sites[2][2].occupy_site()
    assert wm.sites[2][2].occupied is True
    wm.sites[2][2].free_site()
    assert wm.sites[2][2].occupied is False

    assert wm.check_sites_buildable((0, 3), (0, 3)) is True
    """Should be empty and buildable. o is open, x is occupied:
      0 1 2 3
    0 o o o o
    1 o o o o 
    2 o o o o 
    3 o o o o
    """

    test_structure = Structure((2, 2))

    assert wm.build_structure(site=(2, 2), structure=test_structure) is True
    """Should be occupied from 2,2 to 1 1. o is open, x is occupied:
      0 1 2 3
    0 o o o o
    1 o x x o 
    2 o x x o 
    3 o o o o
    """

    assert wm.sites[2][2].structure_anchor == test_structure
    assert wm.sites[0][1].occupied is False
    assert wm.sites[1][0].occupied is False
    assert wm.sites[1][1].occupied is True
    assert wm.sites[0][0].occupied is False
    assert wm.sites[2][1].occupied is True
    assert wm.check_sites_buildable((0, 1), (0, 1)) is True
    assert wm.check_sites_buildable((1, 2), (1, 2)) is False

    assert wm.build_structure(site=(2, 2), structure=test_structure) is False
