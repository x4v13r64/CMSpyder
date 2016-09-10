import datetime
import urllib

import requests
from celery import shared_task

from detection_plugins import get_detection_plugins
from models import Subdomain
from utils import create_logger


# @shared_task
# def discover_type(domain_id):
#     domain = Domain.objects.get(id=domain_id)
#
#     # Create and start logger
#     logger = create_logger(domain_id)
#     logger.info('discover http://{0}'.format(domain.domain))
#
#     domain.type = get_domain_type('http://%s/' % domain.domain)
#
#     logger.info('type for http://{0}/ is {1}'.format(domain.domain, domain.type))
#
#     domain.last_crawl = datetime.datetime.now()
#     domain.save()
#
#
# @shared_task
# def crawl(domain_id):
#     domain = Domain.objects.get(id=domain_id)
#
#     # Create and start logger
#     logger = create_logger(urllib.quote(domain.domain).replace('/', '_'))
#     logger.info('crawl start {0}'.format(domain.url))
#
#     # todo crawl


@shared_task
def detect_cms(subdomain_id):
    subdomain = Subdomain.objects.get(id=subdomain_id)

    if subdomain.subdomain:
        r = requests.get("http://%s.%s.%" %
                         (subdomain.subdomain, subdomain.domain, subdomain.domain.tld))
    else:
        r = requests.get("http://%s.%" %
                         (subdomain.domain, subdomain.domain.tld))

    detection_plugins = get_detection_plugins()
    for plugin in detection_plugins:
        plugin.detect(subdomain, r)
