from datetime import date
from unittest import mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.api.config import API_TICKERS_ENDPOINT, API_HISTORICAL_ENDPOINT, API_CLEAR_ENDPOINT
from app.api.db.models import Ticker, HistoricalData
from app.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
def test_get_ticker_exists(mock_retrieve_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = Ticker(id=1, ticker='BTC-USD')
    response = client.get(url=API_TICKERS_ENDPOINT, params={'ticker_name': ticker.ticker})

    assert response.status_code == status.HTTP_200_OK


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
def test_get_ticker_does_not_exists(mock_retrieve_ticker, client):
    mock_retrieve_ticker.return_value = None
    response = client.get(url=API_TICKERS_ENDPOINT, params={'ticker_name': 'BTC-USD'})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
@mock.patch("app.api.db.crud.retrieve_historical_by_date_range_and_ticker_id", autospec=True)
def test_get_historical_exists_and_ticker_exists(mock_retrieve_historical, mock_retrieve_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = ticker
    mock_retrieve_historical.return_value = [
        HistoricalData(
            date=date(2021, 10, 5).isoformat(),
            ticker_id=1,
            low=25000.00,
            high=35000.00,
            open=27500.00,
            close=32000.00,
            volume=5000.00
        )
    ]
    start = date(2021, 9, 1)
    end = date(2021, 10, 31)
    data_format = 'json'
    response = client.get(url=API_HISTORICAL_ENDPOINT, params={
        'ticker_name': ticker.ticker, 'start': start.isoformat(), 'end': end.isoformat(), 'data_format': data_format
    })

    assert response.status_code == status.HTTP_200_OK


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
@mock.patch("app.api.db.crud.retrieve_historical_by_date_range_and_ticker_id", autospec=True)
def test_get_historical_does_not_exists_and_ticker_exists(mock_retrieve_historical, mock_retrieve_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_historical.return_value = []
    start = date(2021, 9, 1)
    end = date(2021, 10, 31)
    data_format = 'json'
    response = client.get(url=API_HISTORICAL_ENDPOINT, params={
        'ticker_name': ticker.ticker, 'start': start.isoformat(), 'end': end.isoformat(), 'data_format': data_format,
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
@mock.patch("app.api.db.crud.retrieve_historical_by_date_range_and_ticker_id", autospec=True)
def test_get_historical_exists_and_ticker_does_not_exist(mock_retrieve_historical, mock_retrieve_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = None
    mock_retrieve_historical.return_value = [
        HistoricalData(
            date=date(2021, 10, 5).isoformat(),
            ticker_id=1,
            low=25000.00,
            high=35000.00,
            open=27500.00,
            close=32000.00,
            volume=5000.00
        )
    ]
    start = date(2021, 9, 1)
    end = date(2021, 10, 31)
    data_format = 'json'
    response = client.get(url=API_HISTORICAL_ENDPOINT, params={
        'ticker_name': ticker.ticker, 'start': start.isoformat(), 'end': end.isoformat(), 'data_format': data_format,
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mock.patch("app.api.db.crud.create_ticker", autospec=True)
@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
def test_create_ticker(mock_retrieve_ticker, mock_create_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = None
    mock_create_ticker.return_value = ticker
    response = client.post(url=API_TICKERS_ENDPOINT, json={'ticker_name': ticker.ticker})

    assert response.status_code == status.HTTP_200_OK


@mock.patch("app.api.db.crud.create_ticker", autospec=True)
@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
def test_create_ticker_already_(mock_retrieve_ticker, mock_create_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    mock_retrieve_ticker.return_value = ticker
    mock_create_ticker.return_value = None
    response = client.post(url=API_TICKERS_ENDPOINT, json={'ticker_name': ticker.ticker})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
@mock.patch("app.api.db.crud.create_historical", autospec=True)
def test_add_historical_and_ticker_exists(mock_create_historical, mock_retrieve_ticker, client):
    ticker = Ticker(id=1, ticker='BTC-USD')
    json_data = {
      "ticker_name": ticker.ticker,
      "candlestick_records": [
            {
                "date": "2022-02-02",
                "low": 10000,
                "high": 20000,
                "open": 140000,
                "close": 18000,
                "volume": 2234444
            }
        ]
    }
    mock_retrieve_ticker.return_value = ticker
    mock_create_historical.return_value = None
    response = client.post(url=API_HISTORICAL_ENDPOINT, json=json_data)

    assert response.status_code == status.HTTP_200_OK


@mock.patch("app.api.db.crud.retrieve_ticker_by_name", autospec=True)
@mock.patch("app.api.db.crud.create_historical", autospec=True)
def test_add_historical_and_ticker_does_not_exists(mock_create_historical, mock_retrieve_ticker, client):
    json_data = {
      "ticker_name": 'BTC-USD',
      "candlestick_records": [
            {
                "date": "2022-02-02",
                "low": 10000,
                "high": 20000,
                "open": 140000,
                "close": 18000,
                "volume": 2234444
            }
        ]
    }
    mock_retrieve_ticker.return_value = None
    mock_create_historical.return_value = None
    response = client.post(url=API_HISTORICAL_ENDPOINT, json=json_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mock.patch("app.api.db.crud.delete_all_ticker_records", autospec=True)
@mock.patch("app.api.db.crud.delete_all_historical_records", autospec=True)
def test_get_ticker_exists(mock_delete_historical, mock_delete_tickers, client):
    mock_delete_historical.return_value = 10
    mock_delete_tickers.return_value = 1
    response = client.delete(url=API_CLEAR_ENDPOINT)

    assert response.status_code == status.HTTP_200_OK
