import logging
import sys


NAME = 'top-sites-check'
LOGGER = None


def init_logger():
    global LOGGER, NAME
    logging.getLogger(NAME).setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logging.getLogger(NAME).addHandler(ch)
    LOGGER = logging.getLogger(NAME)


def logger():
    global LOGGER
    if LOGGER is None:
        init_logger()
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
