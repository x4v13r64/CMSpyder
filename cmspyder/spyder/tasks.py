from django.conf import settings

from utils import get_domain_type, create_logger
from models import Domain

from celery import task
import urllib


@task()
def discover_type(domain_id):
    domain = Domain.objects.get(id=domain_id)
    domain.type = get_domain_type('http://%s' % domain)
    domain.save()


@task()
def crawl(domain_id):
    domain = Domain.objects.get(id=domain_id)

    # Create and start logger
    logger = create_logger(urllib.quote(domain.domain).replace('/', '_'))
    logger.info('crawl start {0}'.format(domain.url))

    # todo crawl
