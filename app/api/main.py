import datetime
import logging
from logging.config import dictConfig

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse, JSONResponse

from app.api import apiutils
from app.api import crud
from app.api.customdocs import description, tags_metadata
from app.api.database import engine, Base
from app.api.models import HistoricalData
from app.api.schemas import GetHistoricalDataOutputType, PostTickerRequest, PostHistoricalDataRequest
from app.logging.logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("logger")
Base.metadata.create_all(bind=engine)


app = FastAPI(
    docs_url='/',
    title='Crypto Market Data Rest API',
    description=description,
    openapi_tags=tags_metadata
)


@app.get('/ticker/get/', tags=['Tickers'])
def get_ticker(ticker_name: str):
    """
    FastAPI endpoint for getting a cryptocurrency ticker_name if it exists

    :param ticker_name: The ticker_name of interest
    :return: JSONResponse (status code 200) if a ticker_name record exists, HTTPException (status code 404) otherwise
    """
    ticker_record = crud.retrieve_ticker_by_name(ticker_name=ticker_name)
    if ticker_record:
        ticker_json = jsonable_encoder(ticker_record)
        logger.info(f'Ticker record {ticker_json} has been successfully retrieved.')
        return JSONResponse(content=ticker_json)

    message_ticker_missing = f'Ticker {ticker_name} does not exist.'
    logger.error(message_ticker_missing)
    raise HTTPException(status_code=404, detail=message_ticker_missing)


@app.get('/historical/get/', tags=['Historical Data'])
def get_historical(
        ticker_name: str,
        data_format: GetHistoricalDataOutputType,
        start: datetime.date,
        end: datetime.date
):
    """
    FastAPI endpoint for retrieving historical data given a ticker_name and a date range

    :param ticker_name:The ticker_name for which to get the historical data
    :param data_format: Enum - either csv or json
    :param start: The start date
    :param end: The end date
    :return: JSONResponse (status code 200) if a ticker_name record exists and there is historical data related to it
    :raise: HTTPException (status code 404) if such a ticker record does not exist or there is no historical tied to it
    """
    ticker_record = crud.retrieve_ticker_by_name(ticker_name=ticker_name)
    if ticker_record:
        historical_data = crud.retrieve_historical_by_date_range_and_ticker_id(
            start=start, end=end, ticker_id=ticker_record.id
        )
        records_df = apiutils.process_historical_records_to_df(historical_data)
        apiutils.add_pct_change(records_df, HistoricalData.close.name)

        if not records_df.empty:
            logger.info(
                f'Successfully retrieved {len(records_df.index)} {ticker_name} '
                f'records as {data_format} for the following date range: {start} - {end}'
            )
            if data_format == GetHistoricalDataOutputType.csv_format:
                return PlainTextResponse(content=records_df.to_csv(), media_type='text/csv')
            else:
                return JSONResponse(content=records_df.to_dict(orient='records'))

        message_no_records_found = f'No {ticker_name} records found for the following date range: {start} - {end}'
        logger.error(message_no_records_found)
        raise HTTPException(status_code=404, detail=message_no_records_found)

    message_missing_ticker = f'Ticker {ticker_name} does not exist.'
    logger.error(message_missing_ticker)
    raise HTTPException(status_code=404, detail=message_missing_ticker)


@app.post('/ticker/add/', tags=['Tickers'])
def add_ticker(ticker_request: PostTickerRequest):
    """
    FastAPI endpoint for adding a ticker_name, given a string to represent it

    :param ticker_request: Pydantic model with a str attribute
    :return: JSONResponse (status code 200) if the ticker can be added (such a ticker_name record does not yet exist)
    :raise: HTTPException (status code 400) if such a ticker already exists
    """
    ticker_record = crud.retrieve_ticker_by_name(ticker_name=ticker_request.ticker_name)
    if not ticker_record:
        added_ticker = crud.create_ticker(ticker_name=ticker_request.ticker_name)
        ticker_record_json = jsonable_encoder(added_ticker)
        logger.info(f'Ticker record {ticker_record_json} has been successfully added.')
        return JSONResponse(content=ticker_record_json)

    message_ticker_exists = f'Ticker {ticker_request.ticker_name} already exists.'
    logger.error(message_ticker_exists)
    raise HTTPException(status_code=400, detail=message_ticker_exists)


@app.post('/historical/add/', tags=['Historical Data'])
def add_historical(post_historical_request: PostHistoricalDataRequest):
    """
    FastAPI endpoint for adding historical data given a ticker_name and data associated with it

    :param post_historical_request: Pydantic model which has a number of attributes which define what a successful post
    request for submitting historical data should look like
    :return: JSONResponse (status code 200) if the ticker exists and all the historical data that has been added
    :raises: HTTPException (status code 404) if such a ticker does not exist
    """
    ticker_record = crud.retrieve_ticker_by_name(ticker_name=post_historical_request.ticker_name)
    if ticker_record:
        records = apiutils.generate_historical_data_records(ticker_record.id, post_historical_request)
        records_json = [jsonable_encoder(x) for x in records]
        crud.create_historical(records=records)
        logger.info(f'Successfully added {len(records)} {post_historical_request.ticker_name} records.')
        return JSONResponse(
            content={
                'ticker_name': post_historical_request.ticker_name, 'added_records': records_json
            }
        )

    message_missing_ticker = f'Ticker {post_historical_request.ticker_name} ' \
                             f'does not exist - the historical data could not be added.'
    logger.error(message_missing_ticker)
    raise HTTPException(status_code=404, detail=message_missing_ticker)


@app.delete('/records/remove/all', tags=['Database'])
def remove_all_records():
    """
    FastAPI endpoint for clearing all records in the tickers and historical database tables

    :return: JSONResponse (status code 200) with the number of rows that have been deleted form each table
    """
    removed_tickers = crud.delete_all_ticker_records()
    removed_historical_data = crud.delete_all_historical_records()
    message_removed_records = f'Successfully removed {removed_tickers} ticker rows and {removed_historical_data} ' \
                              f'historical data rows.'
    logger.info(message_removed_records)
    return JSONResponse(
        content={'removed_ticker_rows': removed_tickers, 'removed_historical_data_rows': removed_historical_data}
    )
