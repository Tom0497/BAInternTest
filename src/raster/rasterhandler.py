from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional, Dict

import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats

from src.utils import get_raster_filepaths


class RasterHandler:

    def __init__(self, raster_dir: Union[str, Path], vector_file: Union[str, Path]):
        """
        Constructor of RasterHandler object.

        :param raster_dir:
            folder path (str or pathlib.Path) of raster files (.tif).
        :param vector_file:
            path (str or pathlib.Path) of vector layer file (.geojson).
        """

        self._raster_dir = raster_dir
        self._vector_file = vector_file

        self._raster_paths = get_raster_filepaths(raster_dir, True)
        self._gdf = gpd.read_file(vector_file)

    def construct_time_series(self, stats: List[str], trail_str: Optional[str]) -> Dict[str, pd.DataFrame]:
        """
        Construct time series using one or more statistics from rasters zones.

        :param stats:
            statistics to compute for each raster zone (see rasterstats.zonal_stats for options).
        :param trail_str:
            prefix of raster filenames to remove in order to get datetime.

        :return:

        """

        datetimes = self.__get_datetimes(trail_str)
        sector_names = self._gdf['Name']

        df_dict = {stat: pd.DataFrame(index=datetimes, columns=sector_names) for stat in stats}

        for idx, path in enumerate(self._raster_paths):
            res = zonal_stats(str(self._vector_file), str(path), stats=stats)
            for stat in stats:
                df_dict[stat].iloc[idx] = [dictres.get(stat, 0) for dictres in res]

        return df_dict

    def __get_datetimes(self, trail_str: Optional[str]) -> List[datetime]:
        """
        :return:
            cleaned filenames transformed into datetimes objects.
        """

        datetime_list = []
        if not trail_str:
            trail_str = ''

        for path in self._raster_paths:
            strpath = str(path.name)
            datetimestr = strpath.removeprefix(trail_str).removesuffix('.tif')

            dt = datetime.strptime(datetimestr, '%Y-%m-%d')
            datetime_list.append(dt)

        return datetime_list


if __name__ == '__main__':
    import definitions

    rh = RasterHandler(definitions.RASTER_DIR, definitions.VECTORS_DIR / 'agrospace_piloto.geojson')
    series = rh.construct_time_series(['mean', 'std'], 'agrospace_piloto_')
