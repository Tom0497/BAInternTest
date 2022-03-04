"""
definitions.py:
    This file is at the root of the project and contains essential data that remains constant.
"""

import os
from pathlib import Path

"""
Relevant paths for the project.
    ROOT_DIR     - root path of the project
    ASSETS_DIR   - path where files (raster and vectors) are stored
    RASTER_DIR   - path where raster files are
    VECTORS_DIR  - path where vectors files are
    SERIES_DIR   - path to store constructed time series
"""
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = ROOT_DIR / 'assets'
RASTER_DIR = ASSETS_DIR / 'rasterv2'
VECTORS_DIR = ASSETS_DIR / 'shape'
SERIES_DIR = ASSETS_DIR / 'timeseries'
