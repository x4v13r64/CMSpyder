from django.conf import settings

from utils import get_domain_type, create_logger
from models import Domain

from celery import shared_task
import urllib


@shared_task
def discover_type(domain_id):
    domain = Domain.objects.get(id=domain_id)

    # Create and start logger
    logger = create_logger(domain_id)
    logger.info('discover http://{0}'.format(domain.domain))

    domain.type = get_domain_type('http://%s/' % domain.domain)

    logger.info('type for http://{0}/ is {1}'.format(domain.domain, domain.type))

    domain.save()


@shared_task
def crawl(domain_id):
    domain = Domain.objects.get(id=domain_id)

    # Create and start logger
    logger = create_logger(urllib.quote(domain.domain).replace('/', '_'))
    logger.info('crawl start {0}'.format(domain.url))

    # todo crawl
