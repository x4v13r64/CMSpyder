import datetime
import urllib

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from detection_plugins import get_detection_plugins
from domains.models import Subdomain
from models import ScanError
from utils import create_logger


# @shared_task
# def discover_domains(subdomain, request_results):
#
#     # Create and start logger
#     logger = create_logger(urllib.quote(subdomain.id)
#
#     logger.info('domain_discover start {0}'.format(subdomain))
#
#     for request_result in request_results:
#
#
#
#
#     return 1


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
                        requests.get(u"http://%s%s" % (subdomain, path),
                                     verify=False,
                                     timeout=10)
                except requests.exceptions.HTTPError as e:
                    ScanError.objects.create(type='HTTP error',
                                             subdomain=subdomain,
                                             error=u"{}\n{}".format(subdomain, e))
                except requests.exceptions.Timeout:
                    ScanError.objects.create(type='timeout',
                                             subdomain=subdomain)
                except requests.exceptions.TooManyRedirects:
                    ScanError.objects.create(type='redirect limit',
                                             subdomain=subdomain)
                # Tell the user their URL was bad and try a different one
                except requests.exceptions.RequestException as e:
                    ScanError.objects.create(type='request',
                                             subdomain=subdomain,
                                             error=u"{}".format(e))
                except Exception, e:
                    ScanError.objects.create(type='general',
                                             subdomain=subdomain,
                                             error=u"{}".format(e))

    # discover new domains
    discover_domains.delay(subdomain, request_results)

    # fingerprint CMSs
    for plugin in detection_plugins:
        plugin.detect(subdomain, request_results)
