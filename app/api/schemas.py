import datetime
from enum import Enum

from pydantic import BaseModel


class GetHistoricalDataOutputType(str, Enum):
    """
    Enum which clearly defines the types of output to be supported by a GET historical data request
    """
    json_format = 'json'
    csv_format = 'csv'


class CandleStickRecord(BaseModel):
    """
    Pydantic model which represents the concept of a candlestick from financial timeseries analysis - a candlestick is
    a collection of price data points of a tradable asset over a given period of time

    """
    date: datetime.date
    low: float
    high: float
    open: float
    close: float
    volume: float


class PostTickerRequest(BaseModel):
    """
    Pydantic model which defines the acceptable format of data in the case of POST requests when sending new ticker_name
    that is to be written to the database
    """
    ticker_name: str


class PostHistoricalDataRequest(BaseModel):
    """
    Pydantic model which defines the acceptable format of data in the case of POST requests when sending new historical
    data that is to be written to the database
    """
    ticker_name: str
    candlestick_records: list[CandleStickRecord]
