"""Registry for all structures."""

from dataclasses import dataclass
from grid_view.world_model import BuildingType, BuildingModel


@dataclass(frozen=True)
class BuildingView:
    """Type for encapsulting the view information about a building."""

    building_type: BuildingType
    building_name: str
    sprite_path: str
    footprint_path: str


building_view_registry = [
    BuildingView(
        building_type=BuildingType.SHACK,
        building_name="Shack",
        sprite_path="assets/shack.png",
        footprint_path="assets/selected_2x2.png",
    ),
    BuildingView(
        building_type=BuildingType.PLANTER,
        building_name="Planter",
        sprite_path="assets/planter.png",
        footprint_path="assets/selected_1x1.png",
    ),
]

building_view_by_type = {sr.building_type.value: sr for sr in building_view_registry}

building_model_registry = [
    BuildingModel(building_type=BuildingType.SHACK, footprint=(2, 2)),
    BuildingModel(building_type=BuildingType.PLANTER, footprint=(1, 1)),
]

building_model_by_type = {bm.building_type.value: bm for bm in building_model_registry}
