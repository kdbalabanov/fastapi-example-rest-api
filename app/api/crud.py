from datetime import date

from app.api.database import SessionLocal
from app.api.models import Ticker, HistoricalData

db = SessionLocal()


def retrieve_ticker_by_name(ticker_name: str) -> Ticker:
    """
    Given a ticker_name name (unique), get a ticker_name record

    :param ticker_name: Name of the ticker_name
    :return: Ticker record if it exists, None otherwise
    """
    return db.query(Ticker).filter(Ticker.ticker == ticker_name).first()


def retrieve_historical_by_date_range_and_ticker_id(start: date, end: date, ticker_id: int) -> list[HistoricalData]:
    """
    Given a date range and a ticker_name id, get all relevant historical data according to those details

    :param start: Start date
    :param end: End date
    :param ticker_id: Ticker id
    :return: List of HistoricalData records that meet the criteria
    """
    return db.query(HistoricalData).filter(HistoricalData.date >= start). \
        filter(HistoricalData.date <= end). \
        filter(HistoricalData.ticker_id == ticker_id)


def create_ticker(ticker_name: str) -> Ticker:
    """
    Given a ticker_name name, create a ticker_name record and insert it into the database

    :param ticker_name: The name of the ticker_name
    :return: Ticker record that was written to the database
    """
    ticker_record = Ticker()
    ticker_record.ticker = ticker_name
    db.add(ticker_record)
    db.commit()
    db.refresh(ticker_record)
    return ticker_record


def create_historical(records: list[HistoricalData]):
    """
    Given a list of historical data records, add them to the database

    :param records: List of historical data records
    :return: The historical data records which were saved to the database
    """
    db.add_all(records)
    db.commit()


def delete_all_ticker_records() -> int:
    """
    Delete all ticker_name records

    :return: The number of deleted ticker records
    """
    num_removed_tickers = db.query(Ticker).delete()
    db.commit()
    return num_removed_tickers


def delete_all_historical_records() -> int:
    """
    Delete all historical data records

    :return: The deleted historical data records
    """
    num_removed_historical_data = db.query(HistoricalData).delete()
    db.commit()
    return num_removed_historical_data
