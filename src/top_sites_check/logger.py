import logging
import sys
from top_sites_check import consts


def init_logger(log_level=logging.DEBUG):
    logging.getLogger(consts.NAME).setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(consts.LOGGING_FORMAT)
    ch.setFormatter(formatter)
    logging.getLogger(consts.NAME).addHandler(ch)
    consts.LOGGER = logging.getLogger(consts.NAME)


def logger():
    if consts.LOGGER is None:
        init_logger()
    return consts.LOGGER


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
