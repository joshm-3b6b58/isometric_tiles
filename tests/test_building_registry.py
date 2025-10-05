"""Test the building registry."""

from grid_view.building_registry import building_registry_by_type


def test_structure_registry_by_type():
    """Test that the structure registry by type is correct."""
    assert len(building_registry_by_type) == 2
    print(building_registry_by_type)
    assert building_registry_by_type[1].building_name == "Shack"
    assert building_registry_by_type[2].building_name == "Planter"
