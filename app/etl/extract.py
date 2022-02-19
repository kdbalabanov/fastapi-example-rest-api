from datetime import date

import requests

from app.etl import logger


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
    logger.log_api_response(status_code=response.status_code, source=url, response_data=response.json())
    return response
