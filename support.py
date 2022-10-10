import logging
from settings import *

handlers=[
    logging.FileHandler(LOG_FILE_NAME, 'a+'),
    logging.StreamHandler()
]

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=handlers)

def log(msg, level=logging.INFO):
    logging.log(level, msg)