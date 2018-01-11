import logging
import time
from argparse import ArgumentParser
from top_sites_check.backend import QueryService
from top_sites_check.logger import init_logger, error


description = "Run a server that checks if domain is in the top 1m"
config_help = 'configuration file (see sample config in $project/configs'
logging_fmt = 'log levels: INFO: %d, DEBUG: %d, WARRNING: %d'
parser = ArgumentParser(description=description)

parser.add_argument('-config', type=str, default=None, help=config_help)

V = logging_fmt % (logging.INFO,
                   logging.DEBUG,
                   logging.WARNING)
parser.add_argument('-log_level', type=int, default=logging.DEBUG,
                    help=V)

if __name__ == "__main__":
    args = parser.parse_args()

    init_logger(args.log_level)

    if args.config is None:
        error("No configuration specified")
        parser.print_help()

    qs = None
    try:
        qs = QueryService.parse_toml_file(args.config)
        qs.load_start()
        while True:
            time.sleep(60000)
    except KeyboardInterrupt:
        pass
    except:
        raise
    finally:
        if qs is not None:
            qs.stop()
