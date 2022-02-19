import logging
from logging.config import dictConfig

from app.logging.logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("logger")


def log_api_response(status_code: int, source: str, response_data: str):
    """
    Log according to API response status code, customise message with relevant details

    :param status_code: The status code of the response that we received from the API
    :param source: The full URL/endpoint to which a request was sent
    :param response_data: The response data which was returned
    """
    message = f'Received {status_code} response from {source}: \n{response_data}'
    if status_code == 200:
        logger.info(message)
    else:
        logger.error(message)
