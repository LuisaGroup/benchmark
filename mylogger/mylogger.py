import logging
import os

log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs', 'log.log')
if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))


def clear_log_file() -> bool:
    try:
        with open(log_file, 'w') as f:
            return True
    except:
        return False


log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)

logger = logging.getLogger(__file__)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
