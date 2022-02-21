from datetime import date

import pandas

from app.etl import extract
from app.etl import load
from app.etl import transform


def run():
    # Retrieve historical data from Coinbase API
    start = date(2021, 9, 1)
    end = date(2021, 10, 31)
    ticker = 'BTC-USD'
    response = extract.coinbase_api_get_historical(ticker=ticker, start=start, end=end)

    if response.status_code == 200:
        # Send retrieved data to the custom API sa that it is written to the database
        historical_df = pandas.DataFrame(
            data=response.json(),
            columns=['date', 'low', 'high', 'open', 'close', 'volume']
        )
        transform.transform_coinbase_data(historical_df=historical_df)
        load.api_post_ticker(ticker=ticker)
        load.api_post_historical(ticker=ticker, df=historical_df)

        # Attempt to get the historical data through the API in both json and csv formats
        load.api_get_historical(ticker=ticker, start=start, end=end, data_format='json')
        load.api_get_historical(ticker=ticker, start=start, end=end, data_format='csv')


if __name__ == "__main__":
    run()
