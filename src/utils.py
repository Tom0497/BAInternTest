from pathlib import Path
from typing import Union, List

import definitions


def get_raster_filepaths(folder_path: Union[str, Path], sort: bool = True) -> List[Path]:
    """
    Get paths of TIFF files within a specified folder.

    :param folder_path:
        path expected to represent a folder.
    :param sort:
        whether to sort path's list before returning.

    :return:
        list with found paths, empty otherwise.
    """

    if isinstance(folder_path, str):  # if path passed as a string, transform to pathlib.Path
        folder_path = Path(folder_path)

    if not folder_path.is_dir():  # no results if path does not represent a directory
        return []

    tiff_paths = [path for path in folder_path.glob('*.tif')]  # files with .tif extension within folder
    if sort:  # sort paths by their name (ascendant)
        sorted(tiff_paths)

    return tiff_paths


if __name__ == '__main__':
    raster_paths = get_raster_filepaths(definitions.RASTER_DIR, True)
    print(raster_paths)
