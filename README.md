# Crypto Market Data Rest API

This project extracts data from [coinbase API](https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles), and saves it in the DB via the API. 

## Getting Started

Clone this repository.

## How to Run/Deploy (Local Machine - tested on Windows 10)

### Prerequisites

Things you will need to have installed:
```
Python 3.9
```

The PyCharm IDE is recommended.

### Installing

Navigate to the root of the project and execute the following command to install the related dependencies:

```
pip install -r requirements.txt
```

### Deployment

Navigate to the root of the project and execute the following command to run the API:

```
uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

Alternatively, you can run this command so that the API reloads automatically when there are code changes:

```
uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Either way, you should be able to access the FastAPI API through your browser by visiting:
```
http://127.0.0.1:8000
```
It is highly recommended to at least consider interacting with the API through the browser as FastAPI's out of the box
functionalities make it incredibly convenient. The built-in UI docs element allows interactive exploration, calling and 
testing the API directly from the browser. You can read more here: https://fastapi.tiangolo.com/features/


You can then run the app/etl/main.py script.

This script will populate the SQLite database with some historical data for "BTC-USD" by communicating with the API.
The script pulls BTC-USD data from the Coinbase API for the date range 1.9.2021 - 31.10.2021 (for demo purposes), after which it sends a POST request to the custom API to store that data.
At the end it fetches the data that was previously stored in the two supported formats: json and csv.

## Optional Alternative Deployment with Docker (tested on Windows 10 + Docker Desktop)

Navigate to the root of the project and execute the following command to build and run a Docker container:

```
docker-compose up --build
```

This should automatically build and run a Docker container called "fastapi-project-container" and the FastAPI API will automatically start to run.

If you want to, you should be able to access the FastAPI API (which runs in the Docker container) through your local machine's browser by visiting:
```
http://127.0.0.1:8000
```

You can then run the app/etl/main.py script by running the command:
```
python app/etl/main.py
```

This script will populate the SQLite database with some historical data for "BTC-USD" by communicating with the API.

## Running the tests

The pytest testing framework was used. The unit tests can be executed by navigating to the root of the project and using the following commands:
```
python -m pytest app/
```

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

## Acknowledgments

* FastAPI Documentation: https://fastapi.tiangolo.com/
* SQLAlchemy Documentation: https://docs.sqlalchemy.org/
