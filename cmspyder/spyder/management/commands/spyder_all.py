from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.tasks import detect_cms

import amqp
import os

from django.conf import settings


class Command(BaseCommand):
    help = 'Spyder all the subdomains in the database'

    def handle(self, *args, **options):

        print "Checking job count"

        # get the number of jobs currently running
        conn = amqp.Connection(host='%s:%s' % (os.environ['RABBIT_MQ_HOST'],
                                               os.environ['RABBIT_MQ_PORT'],),
                               userid='%s' % os.environ['RABBIT_MQ_USER'],
                               password='%s' % os.environ['RABBIT_MQ_PASSWORD'],
                               virtual_host="/",
                               insist=False)

        chan = conn.channel()
        name, jobs, consumers = chan.queue_declare(queue=settings.CELERY_DEFAULT_QUEUE,
                                                   passive=True)

        # if under 10k jobs, send 100k jobs
        if jobs < 1000:
            print "%s jobs: Will add 100k jobs" % jobs
            # scan subdomains according to oldest last_scan entry
            for subdomain in Subdomain.objects.order_by('last_scan')[:100000]:
                detect_cms.delay(subdomain.id)
            return 1
        else:
            print "%s jobs: skipping" % jobs
            return 0
