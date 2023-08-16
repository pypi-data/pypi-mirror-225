import os

import logging
import math
from pathlib import Path



log = logging.getLogger(__name__)


class Tiles():
    row : str
    col : str
    width : str
    height : str
    x_offset : str
    y_offset : str
    xmin : str
    xmax : str
    ymin : str
    ymax : str
    pixel_size : str
    tile_folder: Path
    tile_multiband_composite: Path


def setup_tiles(aoi_xmin, aoi_xmax, aoi_ymin, aoi_ymax, pixel_size, tiles_parentdir, max_tile_size = 3000):

    if not Path(tiles_parentdir).exists():
        os.makedirs(tiles_parentdir)

    # Calculate xmax and ymin based on the pixel size and number of columns and rows
    num_cols = math.ceil((aoi_xmax - aoi_xmin) / pixel_size)
    num_rows = math.ceil((aoi_ymax - aoi_ymin) / pixel_size)
    # Returns a dictionary of tile infos that can be used to cut a large raster into smaller tiles.
    # Each item in the dictionary has properties:
    # row, column, width_pixels, height_pixels, x_offset_pixels, y_offset_pixels, ulx_coordinate, uly_coordinate
    n_tile_cols = math.ceil(num_cols / max_tile_size)
    n_tile_rows = math.ceil(num_rows / max_tile_size)
    log.debug(f"ntiles: {n_tile_rows}, {n_tile_cols}")

    last_col = n_tile_cols - 1
    last_row = n_tile_rows - 1
    tile_infos = []
    for tile_row in range(n_tile_rows):
        tile_height = max_tile_size
        y_offset = tile_row * tile_height
        # Last row is a special case - tile height must be adjusted.
        if tile_row == last_row:
            tile_height = num_rows - (max_tile_size * tile_row)
        log.debug(f"tile_height {tile_height}")
        for tile_col in range(n_tile_cols):
            tile_width = max_tile_size
            x_offset = tile_col * tile_width
            # Last column is a special case - tile width must be adjusted.
            if tile_col == last_col:
                tile_width = num_cols - (max_tile_size * tile_col)

            # tile_ulx and tile_uly are the absolute coordinates of the upper left corner of the tile.
            tile_ulx = aoi_xmin + x_offset * pixel_size
            tile_uly = aoi_ymax - y_offset * pixel_size
            tile_lrx = tile_ulx + tile_width * pixel_size
            tile_lry = tile_uly - tile_height * pixel_size

            tile_work_dir = tiles_parentdir.joinpath("tile_{:03d}_{:03d}".format(
                tile_row + 1, tile_col + 1))
            tile_work_dir.mkdir(parents=True, exist_ok=True)

            tile_multiband_composite = tile_work_dir.joinpath("tile_{:03d}_{:03d}.tif".format(tile_row + 1, tile_col + 1))

            tile_info = Tiles(
                row= tile_row,
                col= tile_col,
                width= tile_width,
                height= tile_height,
                x_offset= x_offset,
                y_offset= y_offset,
                xmin= tile_ulx,
                xmax= tile_lrx,
                ymin= tile_lry,
                ymax= tile_uly,
                pixel_size= pixel_size,
                tile_folder= tile_work_dir,
                tile_multiband_composite = tile_multiband_composite
            )
            tile_infos.append(tile_info)
    return tile_infos

def cut_composite_totile_function(input_data):
    src_filepath = input_data[0]
    tile_extent_path_dict_json = input_data[1]

    tile_infos = json.loads(tile_extent_path_dict_json)

    for tile_name, tile_info in tile_infos.items():
        tile_composite_filepath = Path(tile_info['tile_folder']).joinpath(Path(src_filepath).name)
        if tile_composite_filepath.exists(): continue
        cmd_gdal = ["gdal_translate",
                    "-of", "GTiff",
                    "-co", "COMPRESS=DEFLATE",
                    "-co", "BIGTIFF=YES",
                    "-co", "TILED=YES",
                    "-eco", "-projwin",
                    "{}".format(tile_info['ulx']), "{}".format(tile_info['uly']),
                    "{}".format(tile_info['lrx']), "{}".format(tile_info['lry']),
                    str(src_filepath), str(tile_composite_filepath)]
        cmd_output = subprocess.run(cmd_gdal, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.debug(f"exit code {cmd_output.returncode} --> {cmd_gdal}")
