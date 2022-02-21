import pandas
from fastapi.encoders import jsonable_encoder

from app.api.db.models import HistoricalData
from app.api.schemas import PostHistoricalDataRequest


def process_historical_records_to_df(historical_data: list[HistoricalData]) -> pandas.DataFrame:
    """
    Given a list of database records (which adhere to the HistoricalData model), generate a pandas.DataFrame

    :param historical_data: List of database records (which adhere to the HistoricalData model)
    :return: pandas.DataFrame representation of the aforementioned database records
    """
    records = [jsonable_encoder(record) for record in historical_data]

    return pandas.DataFrame.from_records(
        data=records,
        columns=[
            HistoricalData.date.name,
            HistoricalData.ticker_id.name,
            HistoricalData.low.name,
            HistoricalData.high.name,
            HistoricalData.open.name,
            HistoricalData.close.name,
            HistoricalData.volume.name
        ]
    )


def add_pct_change(df: pandas.DataFrame, column_name: str):
    """
    Add a percentage change column to a pandas.DataFrame given a column name to base the computation on

    :param df: The pandas.DataFrame that is to be modified
    :param column_name: Column name to base the computation of % change on
    """
    df['% change'] = df[column_name].pct_change() * 100
    df.fillna(value=0.00, inplace=True)


def generate_historical_data_records(
        ticker_id: int,
        post_historical_request: PostHistoricalDataRequest
) -> list[HistoricalData]:
    """
    Given a ticker id and a PostHistoricalDataRequest (contains list[CandlestickRecord] - which in turn contain all
    relevant data (date, low, high, open, close etc.), generate a list of objects (adhering to the
    HistoricalData database model) which can then be written to a database table

    :param ticker_id: The ticker id associated with the data
    :param post_historical_request: A Pydantic model which guarantees that the input data adheres to a certain standard
    :return: List of objects which are ready to be written to a database table
    """
    records = []

    for record in post_historical_request.candlestick_records:
        historical_data = HistoricalData()
        historical_data.date = record.date
        historical_data.ticker_id = ticker_id
        historical_data.low = record.low
        historical_data.high = record.high
        historical_data.open = record.open
        historical_data.close = record.close
        historical_data.volume = record.volume
        records.append(historical_data)

    return records
