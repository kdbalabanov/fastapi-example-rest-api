CUSTOM_DOCS_DESCRIPTION = '''
Simple API made possible by FastAPI.

## Tickers

You can **add or retrieve crypto-currency tickers**. 
\nExample: BTC-USD

## Historical Data

You can **add or retrieve cryptocurrency historical data**. 
You can retrieve such data for a specific date range and ticker. Supports day time-frame only.

## Database

You can **clear all cryptocurrency historical data and tickers**.
'''

CUSTOM_DOCS_TAGS_METADATA = [
    {
        'name': 'Tickers',
        'description': 'Add or retrieve cryptocurrency tickers.'
    },
    {
        'name': 'Historical Data',
        'description': 'Add or retrieve cryptocurrency historical data.'
    },
    {
        'name': 'Database',
        'description': 'Clear all historical data and tickers.'
    }
]

API_HISTORICAL_ENDPOINT = '/historical/'
API_TICKERS_ENDPOINT = '/tickers/'
API_CLEAR_ENDPOINT = '/clear/'
