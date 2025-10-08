"""Test the building registry."""

from grid_view.building_registry import building_view_by_type, building_model_by_type
from grid_view.world_model import BuildingModel, BuildingType


def test_building_view_by_type():
    """Test that the structure registry by type is correct."""
    assert len(building_view_by_type) == 2
    print(building_view_by_type)
    assert building_view_by_type[1].building_name == "Shack"
    assert building_view_by_type[2].building_name == "Planter"


def test_building_model_by_type():
    """Test the functionality of the building model registry."""
    assert building_model_by_type[1] == BuildingModel(
        building_type=BuildingType.SHACK, footprint=(2, 2)
    )
    assert building_model_by_type[1].footprint == (2, 2)


def test_registries_complete():
    """Test that the registries are complete and consistent."""
    assert len(building_view_by_type) == len(set(building_view_by_type.keys()))
    assert len(building_model_by_type) == len(set(building_view_by_type.keys()))
