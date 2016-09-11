import datetime
import urllib

import requests
from celery import shared_task

from detection_plugins import get_detection_plugins
from domains.models import Subdomain
from models import ScanError
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
    # retrieve subdomain object
    subdomain = Subdomain.objects.get(id=subdomain_id)

    # get all detection plugins
    detection_plugins = get_detection_plugins()

    # build dict of request results
    request_results = {}
    for plugin in detection_plugins:
        for path in plugin.paths:
            if path not in request_results:
                try:
                    request_results[path] = \
                        requests.get("http://%s.%s.%s%s" % (subdomain.subdomain,
                                                            subdomain.domain,
                                                            subdomain.domain.tld,
                                                            path) if subdomain.subdomain else
                                     "http://%s.%s%s" % (subdomain.domain,
                                                         subdomain.domain.tld,
                                                         path))
                except Exception, e:
                    ScanError.objects.create(subdomain=subdomain,
                                             error=u"{}\n{}".format(subdomain,
                                                                    e))

    for plugin in detection_plugins:
        plugin.detect(subdomain, request_results)
