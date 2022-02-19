from datetime import date

import pandas
import requests

from app.etl import logger
from app.etl.config import CUSTOM_API_BASE_URL, CUSTOM_API_HISTORICAL_ENDPOINT, CUSTOM_API_TICKERS_ENDPOINT


def api_get_historical(ticker: str, start: date, end: date, data_format: str):
    """
    Given a cryptocurrency ticker, date range and expected data output format, send a GET request to the custom API to
    retrieve historical data

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    :param start: The start date
    :param end: The end date
    :param data_format: The data format that we expect: can be either json or csv
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_HISTORICAL_ENDPOINT
    response = requests.request('GET', url, params={
        'ticker_name': ticker, 'start': start.isoformat(), 'end': end.isoformat(), 'data_format': data_format,
    })
    if data_format == 'json' or response.status_code != 200:
        logger.log_api_response(status_code=response.status_code, source=url, response_data=response.json())
    else:
        logger.log_api_response(status_code=response.status_code, source=url, response_data=response.text)


def api_post_ticker(ticker: str):
    """
    Given a cryptocurrency ticker, send a POST request to the custom API to add the ticker to the records of existing
    tickers

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_TICKERS_ENDPOINT
    response = requests.request('POST', url, json={'ticker_name': ticker})
    logger.log_api_response(status_code=response.status_code, source=url, response_data=response.json())


def api_post_historical(ticker: str, df: pandas.DataFrame):
    """
    Given a cryptocurrency ticker and timeseries data associated with it, send a POST request to the custom API to
    write this historical data to the database

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    :param df: Timeseries data associated with ticker
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_HISTORICAL_ENDPOINT
    response = requests.request(
        'POST', url, json={'ticker_name': ticker, 'candlestick_records': df.to_dict(orient='records')}
    )
    logger.log_api_response(status_code=response.status_code, source=url, response_data=response.json())
