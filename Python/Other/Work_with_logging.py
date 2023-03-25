# ----------------------info----------------------
# LOGGING_CONFIG - словарь, который выносим в отдельный файл в проекте
# formatters - формат логов (много интересных форматов есть)
# handlers - виды обработчиков логов, с уровнем логирования(min) и форматом логирования и файлом для записи логов
# loggers - логгеры, с описанием уровня логирования(min) и handler
# levels of logging :
'''
Level	Numeric value
CRITICAL	50
ERROR	    40
WARNING	    30
INFO	    20
DEBUG	    10
NOTSET	    0 
'''
# ----------------------info----------------------
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(funcName)s: %(message)s'
        }
    },

    'handlers': {
        'infoFileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filename': 'logger.log',
            'formatter': 'default_formatter'
        },
        'errorFileHandler': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'filename': 'logger.log',
            'formatter': 'default_formatter'
            # 'moda': 'a'
        },
    },

    'loggers': {
        'info_logger': {
            'handlers': ['infoFileHandler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'error_logger': {
            'handlers': ['errorFileHandler'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

# ---- use this code to log what you need

logging.config.dictConfig(LOGGING_CONFIG)
logger_info = logging.getLogger('info_logger')
logger_error = logging.getLogger('error_logger')

# logger_info.debug('debug log')
#
# logger_error.error('here error!')

def example(a:int, b:int):
    try:
        c = a // b
        logger_info.info(f'code work nice!{c}')
        return a//b
    except Exception as E:
        logger_error.error(f'Error with a: {a} or b: {b}', E)
        return 1

