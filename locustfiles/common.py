import logging
import os

CONFIG_PATH = os.environ.get('CONFIG_DIR', '../../conf')


# Keeping it simple with the logging formatting
def log_format(logger):
    """Set logging format."""
    formatting = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatting)

    LOG = logging.getLogger(logger)
    return LOG
