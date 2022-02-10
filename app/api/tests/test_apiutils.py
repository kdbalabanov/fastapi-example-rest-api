from datetime import date

import pandas
import pytest
from fastapi.encoders import jsonable_encoder

from app.api import apiutils
from app.api.models import HistoricalData
from app.api.schemas import CandleStickRecord, PostHistoricalDataRequest


@pytest.fixture()
def historical_data():
    return [
        HistoricalData(
            date=date(2021, 10, 5).isoformat(),
            ticker_id=1,
            low=25000.00,
            high=35000.00,
            open=27500.00,
            close=32000.00,
            volume=5000.00
        ),
        HistoricalData(
            date=date(2021, 10, 6).isoformat(),
            ticker_id=1,
            low=26000.00,
            high=36000.00,
            open=28500.00,
            close=33000.00,
            volume=6000.00
        )
    ]


def test_process_historical_records_to_df(historical_data):
    records = [jsonable_encoder(record) for record in historical_data]

    expected_columns = [
        HistoricalData.date.name,
        HistoricalData.ticker_id.name,
        HistoricalData.low.name,
        HistoricalData.high.name,
        HistoricalData.open.name,
        HistoricalData.close.name,
        HistoricalData.volume.name
    ]
    expected_data = [
        [date(2021, 10, 5).isoformat(), 1, 25000.00, 35000.00, 27500.00, 32000.00, 5000.00],
        [date(2021, 10, 6).isoformat(), 1, 26000.00, 36000.00, 28500.00, 33000.00, 6000.00]
    ]

    result_df = apiutils.process_historical_records_to_df(historical_data)
    expected_df = pandas.DataFrame(data=expected_data, columns=expected_columns)
    pandas.testing.assert_frame_equal(expected_df, result_df)


def test_add_pct_change():
    close = 'close'
    pct_change = '% change'

    input_columns = [close]
    input_data = [
        [10000],
        [15000],
        [30000],
        [3000],
        [3300]
    ]

    expected_columns = [close, pct_change]
    expected_data = [
        [10000, 0.00],
        [15000, 50.00],
        [30000, 100.00],
        [3000, -90.00],
        [3300, 10.00]
    ]

    result_df = pandas.DataFrame(data=input_data, columns=input_columns)
    apiutils.add_pct_change(result_df, close)
    expected_df = pandas.DataFrame(data=expected_data, columns=expected_columns)
    pandas.testing.assert_frame_equal(expected_df, result_df)


def test_generate_historical_data_records(historical_data):
    candlestick_records = [
        CandleStickRecord(
            date=date(2021, 10, 5).isoformat(),
            low=25000.00,
            high=35000.00,
            open=27500.00,
            close=32000.00,
            volume=5000.00
        ),
        CandleStickRecord(
            date=date(2021, 10, 6).isoformat(),
            low=26000.00,
            high=36000.00,
            open=28500.00,
            close=33000.00,
            volume=6000.00
        )
    ]
    post_historical_request = PostHistoricalDataRequest(ticker_name='BTC-USD', candlestick_records=candlestick_records)
    result_historical_data = apiutils.generate_historical_data_records(
        ticker_id=1,
        post_historical_request=post_historical_request
    )

    assert jsonable_encoder(result_historical_data) == jsonable_encoder(historical_data)
