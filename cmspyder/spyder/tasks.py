import datetime
import urllib

import requests
from celery import shared_task

from detection_plugins import get_detection_plugins
from domains.models import Subdomain
from models import ScanError
from utils import create_logger

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

    # Create and start logger
    logger = create_logger(subdomain.id)

    # get all detection plugins
    detection_plugins = get_detection_plugins()

    # build dict of request results
    request_results = {}
    # for each path defined in a plugin, if that path hasn't been queried yet, query that path
    # and put the result in the result dict
    for plugin in detection_plugins:
        for path in plugin.paths:
            if path not in request_results:
                try:
                    logger.info('discover http://{0}'.format(subdomain))
                    request_results[path] = \
                        requests.get(u"http://%s%s" % (subdomain.subdomain, path))
                        # requests.get("http://%s.%s.%s%s" % (subdomain.subdomain,
                        #                                     subdomain.domain,
                        #                                     subdomain.domain.tld,
                        #                                     path) if subdomain.subdomain else
                        #              "http://%s.%s%s" % (subdomain.domain,
                        #                                  subdomain.domain.tld,
                        #                                  path))
                except Exception, e:
                    # log scan error
                    ScanError.objects.create(subdomain=subdomain,
                                             error=u"{}\n{}".format(subdomain, e))

    for plugin in detection_plugins:
        plugin.detect(subdomain, request_results)
