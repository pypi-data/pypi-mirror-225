import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
ERROR = logging.ERROR

def basicConfig(level=DEBUG, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename=None):
    logging.basicConfig(level=level, format=format, datefmt=datefmt, filename=filename)

def debug(message):
    logging.debug(message)

def info(message):
    logging.info(message)

def error(message):
    logging.error(message)
