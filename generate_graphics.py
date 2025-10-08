"""Code to generate graphics programmatically."""

from PIL import Image
import numpy as np
from arcade import Vec2

from grid_view.utils import world_to_iso
from grid_view.constants import TILE_SIZE

outline_color = (217, 211, 217, 255)
selected_outline_color = (198, 85, 80, 255)
overlay_outline_color = (225, 201, 122, 255)
selected_fill_color = (225, 201, 122, 100)


def create_square_border_array(
    size, border_width=1, border_color=(255, 255, 255, 255), default_value=(0, 0, 0, 0)
) -> np.ndarray:
    """Create a square array with a border."""
    a = np.full((size, size, 4), default_value, dtype=np.uint8)
    a[0:border_width, :] = border_color  # Top row
    a[-(border_width):, :] = border_color  # Bottom row
    a[:, 0:border_width] = border_color  # Left column
    a[:, -(border_width):] = border_color  # Right column
    return a


def convert_to_isometric(square_array: np.ndarray) -> np.ndarray:
    """Convert an array to isometric projection."""
    input_array_size = square_array.shape
    iso_array_x = int(1.73 * input_array_size[0])
    iso_array_y = input_array_size[1]
    print(iso_array_x, iso_array_y)

    default_value = (0, 0, 0, 0)
    a = np.full((iso_array_x, iso_array_y, 4), default_value, dtype=np.uint8)

    for i in range(input_array_size[0]):
        for j in range(input_array_size[1]):
            color = square_array[i, j]
            new_coord = world_to_iso(Vec2(i, j))
            new_element = (int(new_coord.x + iso_array_x // 2), int(new_coord.y))
            a[new_element] = color

    return a


img = Image.fromarray(create_square_border_array(32, border_width=2))
img.save("assets/output_image.png")

iso_img = Image.fromarray(
    convert_to_isometric(
        create_square_border_array(32, border_width=2, border_color=outline_color)
    )
)
rot_iso_img = iso_img.rotate(90, expand=True)
rot_iso_img.save("assets/grid_cell.png")

iso_img = Image.fromarray(
    convert_to_isometric(
        create_square_border_array(
            TILE_SIZE, border_width=3, border_color=selected_outline_color
        )
    )
)
rot_iso_img = iso_img.rotate(90, expand=True)
rot_iso_img.save("assets/selected_grid_cell.png")


iso_img = Image.fromarray(
    convert_to_isometric(
        create_square_border_array(
            3 * TILE_SIZE,
            border_width=2,
            border_color=overlay_outline_color,
            default_value=selected_fill_color,
        )
    )
)
rot_iso_img = iso_img.rotate(90, expand=True)
rot_iso_img.save("assets/selected_3x3.png")

iso_img = Image.fromarray(
    convert_to_isometric(
        create_square_border_array(
            2 * TILE_SIZE,
            border_width=2,
            border_color=overlay_outline_color,
            default_value=selected_fill_color,
        )
    )
)
rot_iso_img = iso_img.rotate(90, expand=True)
rot_iso_img.save("assets/selected_2x2.png")

iso_img = Image.fromarray(
    convert_to_isometric(
        create_square_border_array(
            TILE_SIZE,
            border_width=2,
            border_color=overlay_outline_color,
            default_value=selected_fill_color,
        )
    )
)
rot_iso_img = iso_img.rotate(90, expand=True)
rot_iso_img.save("assets/selected_1x1.png")
