import logging
from datetime import datetime


def get_base_logger(name):
    """Creates base level logger."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s: %(message)s')  # noqa

    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    try:
        file_name = 'logs/{}.log'.format(datetime.now())
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except: # noqa
        pass

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
