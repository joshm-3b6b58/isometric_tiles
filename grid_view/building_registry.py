"""Registry for all structures."""

from dataclasses import dataclass
from grid_view.world_model import BuildingType


@dataclass(frozen=True)
class Building:
    """Type for encapsulting the view information about a building."""

    building_type: BuildingType
    building_name: str
    sprite_path: str
    foot_print_path: str


building_registry = [
    Building(
        building_type=BuildingType.SHACK,
        building_name="Shack",
        sprite_path="assets/shack.png",
        foot_print_path="assets/selected_2x2.png",
    ),
    Building(
        building_type=BuildingType.PLANTER,
        building_name="Planter",
        sprite_path="assets/planter.png",
        foot_print_path="assets/selected_1x1.png",
    ),
]

building_registry_by_type = {sr.building_type.value: sr for sr in building_registry}
