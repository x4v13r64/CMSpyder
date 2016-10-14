from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.tasks import detect_cms

import amqp
import os

from django.conf import settings


class Command(BaseCommand):
    help = 'Spyder all the subdomains in the database'

    def handle(self, *args, **options):

        conn = amqp.Connection(host='%s:%s' % (os.environ['RABBIT_MQ_HOST'],
                                               os.environ['RABBIT_MQ_PORT'],),
                               userid='%s' % os.environ['RABBIT_MQ_USER'],
                               password='%s' % os.environ['RABBIT_MQ_PASSWORD'],
                               virtual_host="/",
                               insist=False)

        chan = conn.channel()
        name, jobs, consumers = chan.queue_declare(queue=settings.CELERY_DEFAULT_QUEUE,
                                                   passive=True)
        print jobs

        return

        subdomains = Subdomain.objects.filter()
        for subdomain in subdomains:
            detect_cms.delay(subdomain.id)
