import logging.config
import os
import typing as t

from .config import settings

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s\n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join('logs', 'app.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
        },
    },
    'loggers': {
        settings.APP_NAME: {
            'level': settings.LOG_LEVEL,
            'handlers': (['console', 'file']),
        },
    },
    'disable_existing_loggers': False,
}


def init_logging() -> t.NoReturn:
    logging.config.dictConfig(LOGGING_CONFIG)
