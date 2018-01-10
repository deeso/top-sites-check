import logging
import sys


from .csvzip import CsvZipServiceInterface

DATA_SOURCES = {
    CsvZipServiceInterface.key(): CsvZipServiceInterface
}

NAME = 'top-sites-check'
logging.getLogger(NAME).setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logging.getLogger(NAME).addHandler(ch)

LOGGER = logging.getLogger(NAME)


def logger():
    return LOGGER


def debug(msg):
    logger().debug(msg)


def info(msg):
    logger().info(msg)


def warn(msg):
    logger().warn(msg)


def error(msg):
    logger().error(msg)


def critical(msg):
    logger().critical(msg)
