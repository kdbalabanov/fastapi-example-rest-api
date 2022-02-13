import logging
from datetime import date
from logging.config import dictConfig

import pandas
import requests

from app.logging.logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("logger")

CUSTOM_API_BASE_URL = 'http://127.0.0.1:8000'
CUSTOM_API_ADD_TICKER_ENDPOINT = '/ticker/add/'
CUSTOM_API_GET_HISTORICAL_ENDPOINT = '/historical/get/'
CUSTOM_API_ADD_HISTORICAL_ENDPOINT = '/historical/add/'


def log_api_response(status_code: int, source: str, response_data: str):
    """
    Log according to API response status code, customise message with relevant details

    :param status_code: The status code of the response that we received from the API
    :param source: The full URL/endpoint to which a request was sent
    :param response_data: The response data which was returned
    """
    message = f'Received {status_code} response from {source}: \n{response_data}'
    if status_code == 200:
        logger.info(message)
    else:
        logger.error(message)


def coinbase_get_historical(ticker: str, start: date, end: date) -> requests.Response:
    """
    Given a cryptocurrency ticker and date range, send a GET request to the Coinbase API to retrieve historical
    timeseries data and return the response

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    :param start: The start date
    :param end: The end date
    :return: GET request Response from Coinbase API
    """
    url = f'https://api.exchange.coinbase.com/products/{ticker}/candles'
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params={
        'start': start, 'end': end, 'granularity': '1d'
    })
    log_api_response(status_code=response.status_code, source=url, response_data=response.json())
    return response


def transform_coinbase_data(historical_df: pandas.DataFrame):
    """
    Given a pandas.DataFrame containing timeseries data, convert the timestamps to dates of ISO format and sort by date

    :param historical_df: Timeseries data retrieved from Coinbase API
    """
    historical_df['date'] = historical_df['date'].map(lambda x: date.fromtimestamp(x).isoformat())
    historical_df.sort_values(by='date', inplace=True, ignore_index=True)


def api_get_historical(ticker: str, start: date, end: date, data_format: str):
    """
    Given a cryptocurrency ticker, date range and expected data output format, send a GET request to the custom API to
    retrieve historical data

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    :param start: The start date
    :param end: The end date
    :param data_format: The data format that we expect: can be either json or csv
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_GET_HISTORICAL_ENDPOINT
    response = requests.request('GET', url, params={
        'ticker_name': ticker, 'start': start.isoformat(), 'end': end.isoformat(), 'data_format': data_format,
    })
    if data_format == 'json' or response.status_code != 200:
        log_api_response(status_code=response.status_code, source=url, response_data=response.json())
    else:
        log_api_response(status_code=response.status_code, source=url, response_data=response.text)


def api_post_ticker(ticker: str):
    """
    Given a cryptocurrency ticker, send a POST request to the custom API to add the ticker to the records of existing
    tickers

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_ADD_TICKER_ENDPOINT
    response = requests.request('POST', url, json={'ticker_name': ticker})
    log_api_response(status_code=response.status_code, source=url, response_data=response.json())


def api_post_historical(ticker: str, df: pandas.DataFrame):
    """
    Given a cryptocurrency ticker and timeseries data associated with it, send a POST request to the custom API to
    write this historical data to the database

    :param ticker: Cryptocurrency ticker (example BTC-USD)
    :param df: Timeseries data associated with ticker
    """
    url = CUSTOM_API_BASE_URL + CUSTOM_API_ADD_HISTORICAL_ENDPOINT
    response = requests.request(
        'POST', url, json={'ticker_name': ticker, 'candlestick_records': df.to_dict(orient='records')}
    )
    log_api_response(status_code=response.status_code, source=url, response_data=response.json())


def run():
    # Retrieve historical data from Coinbase API
    start = date(2021, 9, 1)
    end = date(2021, 10, 31)
    ticker = 'BTC-USD'
    response = coinbase_get_historical(ticker, start, end)

    if response.status_code == 200:
        # Send retrieved data to the custom API sa that it is written to the database
        historical_df = pandas.DataFrame(response.json(), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        transform_coinbase_data(historical_df)
        api_post_ticker(ticker)
        api_post_historical(ticker, historical_df)

        # Attempt to get the historical data through the API in both json and csv formats
        api_get_historical(ticker, start, end, 'json')
        api_get_historical(ticker, start, end, 'csv')


if __name__ == "__main__":
    run()
