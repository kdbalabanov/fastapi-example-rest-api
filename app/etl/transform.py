from datetime import date

import pandas


def transform_coinbase_data(historical_df: pandas.DataFrame):
    """
    Given a pandas.DataFrame containing timeseries data, convert the timestamps to dates of ISO format and sort by date

    :param historical_df: Timeseries data retrieved from Coinbase API
    """
    historical_df['date'] = historical_df['date'].map(lambda x: date.fromtimestamp(x).isoformat())
    historical_df.sort_values(by='date', inplace=True, ignore_index=True)
