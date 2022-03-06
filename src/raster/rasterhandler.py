from datetime import datetime
from pathlib import Path
from typing import Union, List, Optional, Dict, Tuple

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from rasterstats import zonal_stats
from matplotlib_scalebar.scalebar import ScaleBar

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
        Construct time series using one or more statistics from raster zones.

        :param stats:
            statistics to compute for each raster zone (see rasterstats.zonal_stats for options).
        :param trail_str:
            prefix of raster filenames to remove in order to get datetime.

        :return:
            dict
                key   - (str) statistic name.
                value - (pandas.DataFrame) constructed table with collected data.
        """

        datetimes = self.__get_datetimes(trail_str)
        sector_names = self._gdf['Name']

        df_dict = {stat: pd.DataFrame(index=datetimes, columns=sector_names) for stat in stats}  # initialize dict

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

    def plot_over_map(self) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot sectors specified in feojson over map.

        :return:
            (figure, axes) plot elements.
        """

        fig: plt.Figure
        ax: plt.Axes
        fig, ax = plt.subplots(figsize=(10, 6))  # create plot

        ax = self._gdf.plot("Name",
                            ax=ax,
                            alpha=0.4,
                            edgecolor='k',
                            cmap='tab20',
                            legend=True,
                            legend_kwds=dict(loc='upper left',
                                             bbox_to_anchor=(1, 1),
                                             fancybox=True,
                                             title='Potreros',
                                             title_fontproperties=dict(weight='bold')))
        ax.add_artist(ScaleBar(111.60822260176911, dimension="si-length", units="km"))

        self._gdf.apply(lambda x: ax.annotate(text=f'{x["Sector"]:.0f}-{x["ID"]:.0f}',
                                              xy=x.geometry.centroid.coords[0],
                                              ha='center'), axis=1)
        cx.add_basemap(ax,
                       crs=self._gdf.crs,
                       source=cx.providers.OpenTopoMap)

        fig.tight_layout()
        plt.show()

        return fig, ax


if __name__ == '__main__':
    import definitions

    rh = RasterHandler(definitions.RASTER_DIR, definitions.VECTORS_DIR / 'agrospace_piloto.geojson')
    series = rh.construct_time_series(['mean', 'std'], 'agrospace_piloto_')
    rh.plot_over_map()
