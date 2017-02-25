import os

import amqp
from django.conf import settings
from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.tasks import detect_cms


class Command(BaseCommand):
    help = 'Spyder all the subdomains in the database'

    def handle(self, *args, **options):

        print("Checking job count")

        # get the number of jobs currently running
        """
        conn = amqp.Connection(host='{0}:{1}'.format(os.environ['RABBIT_MQ_HOST'],
                                               os.environ['RABBIT_MQ_PORT'],),
                               userid='{0}'.format(os.environ['RABBIT_MQ_USER']),
                               password='{0}'.format(os.environ['RABBIT_MQ_PASSWORD']),
                               virtual_host="/",
                               insist=False)

        chan = conn.channel()
        name, jobs, consumers = chan.queue_declare(queue=settings.CMSPYDER_DETECT_CMS_QUEUE,
                                                   passive=True)

        # if under 10k jobs, send 100k jobs
        if jobs < 1000:
            print("{0} jobs: Will add 100k jobs".format(jobs))
            # scan subdomains according to oldest last_scan entry
            for subdomain in Subdomain.objects.order_by('last_scan')[:100000]:
                detect_cms.delay(subdomain.id)
        else:
            print("{0} jobs: skipping".format(jobs))
        """

        for subdomain in Subdomain.objects.order_by('last_scan')[:100000]:
            detect_cms.delay(subdomain.id)
