import numpy as np
from numpy.testing import assert_array_equal


from main import world_to_iso, WorldModel, SiteModel
from pytest import approx
from arcade import Vec2


def test_world_to_iso():
    """Test that the isometric conversions are correct for a unit square."""
    assert world_to_iso(Vec2(0, 0)).x == 0
    assert world_to_iso(Vec2(0, 0)).y == 0
    assert world_to_iso(Vec2(1, 0)).x == approx(0.866, rel=1e-3)
    assert world_to_iso(Vec2(1, 0)).y == approx(-0.5, rel=1e-3)
    assert world_to_iso(Vec2(0, 1)).x == approx(0.5, rel=1e-3)
    assert world_to_iso(Vec2(0, 1)).y == approx(0.866, rel=1e-3)
    assert world_to_iso(Vec2(1, 1)).x == approx(0.5 + 0.866, rel=1e-3)
    assert world_to_iso(Vec2(1, 1)).y == approx(0.866 - 0.5, rel=1e-3)


def test_site_model():
    """Test the model for an individual site."""
    site = SiteModel(location=Vec2(0, 0), selected=False)

    assert site.selected is False
    site.disselect()
    assert site.selected is False
    site.select()
    assert site.selected is True
    site.disselect()
    assert site.selected is False


def test_world_model():
    """Test the array representation of the world model."""
    wm = WorldModel(size=2, tile_size=1)
    assert len(wm.sites) == 2
    assert_array_equal(
        wm.sites,
        [
            [SiteModel(Vec2(0, 0)), SiteModel(Vec2(0, 1))],
            [SiteModel(Vec2(1, 0)), SiteModel(Vec2(1, 1))],
        ],
    )
    assert wm.sites[0][0].selected is False
    wm.sites[0][0].select()
    assert wm.sites[0][0].selected is True
