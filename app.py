from flask import Flask
from flask import render_template
from src.raster.rastertimeseries import check_timeseries_exist, construct_time_series, RasterTimeSeries

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route("/data/")
@app.route("/data/<string:stat>")
def data_api(stat=None):
    """
    Generate server response with data.

    :param stat:
        statistic name to query data.

    :return:
        server response to request.
    """

    data = get_data(stat)
    return data


def get_data(stat) -> str:
    """
    Get timeseries data of a statistic as JSON string.

    :param stat:
        statistic name.

    :return:
         timeseries data in JSON format.
    """

    if stat not in ['mean', 'std']:
        stat = 'mean'

    if not check_timeseries_exist(stat):
        construct_time_series([stat])

    rtseries = RasterTimeSeries(stat)
    series_df = rtseries.dataframe
    jsondata = series_df.to_json()

    return jsondata

