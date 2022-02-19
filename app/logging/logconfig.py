from pydantic import BaseModel


class LogConfig(BaseModel):
    """Reusable logging configuration"""

    LOGGER_NAME: str = 'logger'
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'DEBUG'

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers = {
        'logger': {'handlers': ['default'], 'level': LOG_LEVEL},
    }
