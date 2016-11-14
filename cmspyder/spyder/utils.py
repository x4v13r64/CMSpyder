import logging
import os

from django.conf import settings


def create_logger(domain):
    if not os.path.exists(settings.CRAWLER_LOGS_DIR):
        os.makedirs(settings.CRAWLER_LOGS_DIR)
    file_name = os.path.join(settings.CRAWLER_LOGS_DIR,
                             settings.CRAWLER_LOG_FILE_NAME.format(domain))
    logger = logging.getLogger('crawler {0}'.format(domain))
    logger.setLevel(logging.DEBUG)
    # handler = logging.FileHandler(file_name)
    f = logging.Formatter(settings.CRAWLER_LOG_FORMAT)
    # handler.setFormatter(f)
    # logger.addHandler(handler)
    return logger
