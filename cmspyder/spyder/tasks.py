import requests
from bs4 import BeautifulSoup, SoupStrainer
from celery import shared_task
from django.utils import timezone
from fake_useragent import UserAgent

from detection_plugins import get_detection_plugins
from domains.models import Subdomain
from domains.utils import extract_subdomain, get_ip, import_subdomain
from models import ScanError
from utils import create_logger


@shared_task
def discover_domains(subdomain_id, request_result_text):

    # retrieve subdomain object
    subdomain = Subdomain.objects.get(id=subdomain_id)

    # Create and start logger
    logger = create_logger('discover_{0}.log'.format(subdomain.id))

    logger.info('discover {0} START'.format(subdomain.id))

    # keep list or extracted subdomains to limit db queries
    extracted_subdomain = []

    for link in BeautifulSoup(request_result_text, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href') and '://' in link['href']:  # todo improve this
            href = link['href']
            extract_result = extract_subdomain(href)
            if extract_result not in extracted_subdomain:
                extracted_subdomain.append(extract_result)
                new_subdomain = import_subdomain(href,
                                                 discovered_by=subdomain)
                logger.info('discover found {0}'.format(new_subdomain))

    logger.info('discover {0} DONE'.format(subdomain_id))


@shared_task
def detect_cms(subdomain_id):

    ua = UserAgent()

    # retrieve subdomain object
    subdomain = Subdomain.objects.get(id=subdomain_id)

    # Create and start logger
    logger = create_logger('detect_{0}.log'.format(subdomain.id))

    logger.info('detect {0} INIT'.format(subdomain))

    # retrieve ip for subdomain
    subdomain_ip = get_ip(subdomain.__unicode__())

    # update last scan datetime
    subdomain.last_scan = timezone.now()

    if subdomain_ip:

        # update domain ip
        # todo this should be historic (not overwrite
        subdomain.last_ip = subdomain_ip

        # get all detection plugins
        detection_plugins = get_detection_plugins()

        # todo start by resolving IP

        # todo should it iterate on all files after any type of error (e.g. timeout)?

        # build dict of request results
        request_results = {}
        # for each path defined in a plugin, if that path hasn't been queried yet, query
        # that path and put the result in the result dict
        for plugin in detection_plugins:
            for path in plugin.paths:
                if path not in request_results:
                    try:
                        logger.info('detect request {0} START'.format(subdomain))
                        request_results[path] = \
                            requests.get(u"http://%s%s" % (subdomain, path),
                                         verify=False,
                                         timeout=10,
                                         headers={
                                             'User-Agent': ua.random,
                                         })
                        logger.info('detect request {0} DONE'.format(subdomain))
                    except requests.exceptions.HTTPError as e:
                        ScanError.objects.create(type='HTTP error',
                                                 subdomain=subdomain,
                                                 error=u"{}\n{}".format(subdomain, e))
                        logger.info('detect request {0} ERROR HTTPError'.format(subdomain))
                    except requests.exceptions.Timeout:
                        ScanError.objects.create(type='timeout',
                                                 subdomain=subdomain)
                        logger.info('detect request {0} ERROR timeout'.format(subdomain))
                    except requests.exceptions.TooManyRedirects:
                        ScanError.objects.create(type='redirect limit',
                                                 subdomain=subdomain)
                        logger.info('detect request {0} ERROR redirect limit'.format(subdomain))
                    # Tell the user their URL was bad and try a different one
                    except requests.exceptions.RequestException as e:
                        ScanError.objects.create(type='request',
                                                 subdomain=subdomain,
                                                 error=u"{}".format(e))
                        logger.info('detect request {0} ERROR request {1}'.format(subdomain, e))
                    except Exception as e:
                        ScanError.objects.create(type='general',
                                                 subdomain=subdomain,
                                                 error=u"{}".format(e))
                        logger.info('detect request {0} ERROR general {1}'.format(subdomain, e))

        # discover new domains
        logger.info('request {0} discover subtask'.format(subdomain))
        for path in request_results:
            discover_domains.delay(subdomain.id, request_results[path].text)

        # fingerprint CMSs
        logger.info('detect {0} START'.format(subdomain))
        for plugin in detection_plugins:
            plugin.detect(subdomain, request_results)

    else:

        logger.info('detect {0} NO IP'.format(subdomain))

    subdomain.save()

    logger.info('detect {0} DONE'.format(subdomain))
