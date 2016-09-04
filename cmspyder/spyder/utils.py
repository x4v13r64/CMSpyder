import os
import logging
import requests

from bs4 import BeautifulSoup

from django.conf import settings


def is_wordpress(soup):
    meta_tags = soup.find_all('meta', {'name': 'generator'})

    for meta_tag in meta_tags:
        if meta_tag['content'].lower().startswith('wordpress'):
            return True

    css_tags = soup.find_all('link', rel='stylesheet')
    for css_tag in css_tags:
        try:
            if 'wp-content' in css_tag['href'] or 'wp-include' in css_tag['href']:
                return True
        except:
            # Some tags don't have `href`
            pass

    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        try:
            if 'wp-content' in script_tag['src'] or 'wp-include' in script_tag['src']:
                return True
        except:
            # Some tags don't have `src`
            pass

    return False


def get_domain_type(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    if is_wordpress(soup):
        return 'wordpress'
    else:
        return None


def create_logger(domain):
    if not os.path.exists(settings.CRAWLER_LOGS_DIR):
        os.makedirs(settings.CRAWLER_LOGS_DIR)
    file_name = os.path.join(settings.CRAWLER_LOGS_DIR,
                             settings.CRAWLER_LOG_FILE_NAME.format(domain))
    logger = logging.getLogger('crawler %s' % domain)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(file_name)
    f = logging.Formatter(settings.CRAWLER_LOG_FORMAT)
    handler.setFormatter(f)
    logger.addHandler(handler)
    return logger
