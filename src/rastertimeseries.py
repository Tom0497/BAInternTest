from typing import List

import definitions
from src.raster.rasterhandler import RasterHandler


def construct_time_series(statistics: List[str]):
    """
    Construct time series and save them to CSV.

    :param statistics:
        statistics to compute per zone.
    """

    rh = RasterHandler(definitions.RASTER_DIR, definitions.VECTORS_DIR / 'agrospace_piloto.geojson')
    series = rh.construct_time_series(statistics, 'agrospace_piloto_')

    path = definitions.SERIES_DIR
    for stat in statistics:
        filename = f'{stat}.csv'
        savepath = path / filename

        series[stat].to_csv(savepath)


if __name__ == '__main__':
    construct_time_series(['mean'])
