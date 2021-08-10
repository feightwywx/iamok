import logging
from sys import stdout

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stdout)
handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s][%(levelname)s]%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(handler)
