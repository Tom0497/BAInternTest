from typing import List, Dict, Tuple, Optional

import matplotlib.pyplot as plt
import pandas as pd

import definitions
from src.raster.rasterhandler import RasterHandler


class RasterTimeSeries:

    def __init__(self, statistic: str):
        """
        Constructor of RasterTimeSeries object.

        :param statistic:
            name of statistic representing timeseries.
        """

        self._statistic = statistic
        self._valid_statistic = check_timeseries_exist(statistic)
        self._path = definitions.SERIES_DIR / f'{statistic}.csv'

        self._series = pd.read_csv(self._path, index_col=0) if self._valid_statistic else None

    def compute_stats(self) -> Dict:
        """
        :return:
            stats (mean, std, inter-quantile range) per column of pandas.DataFrame.
        """

        if not self._valid_statistic:
            return {}

        res = {}
        columns = self._series.columns
        for column in columns:
            mean = self._series[column].mean()
            std = self._series[column].std()

            q3 = self._series[column].quantile(.75)
            q1 = self._series[column].quantile(.25)
            interquantil = q3 - q1

            res[column] = (mean, std, interquantil)

        return res

    @property
    def datetimes(self) -> List[Tuple]:
        """
        :return:
            list of tuples - (int, datetime) index from pandas.DataFrame.
        """

        if not self._valid_statistic:
            return [()]

        return list(enumerate(self._series.index.tolist()))

    def barplot_by_datetimes(self, datetimes: List[int], ax: Optional[plt.Axes] = None) -> Optional[plt.Axes]:
        """
        Generate a grouped bar plot by selecting existing datetimes by index (see datetimes property).

        :param datetimes:
            list of index representing datetimes to plot.
        :param ax:
            axes where to draw bar plot, optional.

        :return:
            axes where bar plot was drawn.
        """

        if not self._valid_statistic:
            return

        if not ax:
            fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

        sub_df: pd.DataFrame = self._series.iloc[datetimes]
        sub_df.plot.bar(ax=ax, width=.9)

        ax.tick_params(axis='x', labelrotation=0)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_title('NDVI index by date')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', fontsize=6)

        plt.tight_layout()

        return ax


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


def check_timeseries_exist(statistic: str):
    """
    Check if time series of given statistic exists as CSV file.

    :param statistic:
        name of statistic.

    :return:
        whether time series exists.
    """

    filepath = definitions.SERIES_DIR / f'{statistic}.csv'
    return filepath.is_file()


if __name__ == '__main__':
    test_statistic = 'mean'
    construct_time_series([test_statistic])
    print(f"La serie de tiempo {test_statistic} existe: {check_timeseries_exist(test_statistic)}")

    rtseries = RasterTimeSeries(test_statistic)
    rtseries_stats = rtseries.compute_stats()

    available_dates = rtseries.datetimes
    rtseries.barplot_by_datetimes([0, 3])

    plt.show()
