import os

import amqp
from django.conf import settings
from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.models import ScanResult
from spyder.tasks import detect_cms

"""
currently running jobs
total website count
total websites with detection & %
list of all detected CMSs with count & %
list of all CMS versions with count & %

http://stackoverflow.com/questions/3432673/get-distinct-values-of-queryset-by-field
"""


class Command(BaseCommand):
    help = 'Regenerate static website statistics'

    def handle(self, *args, **options):

        # get the number of jobs currently running
        conn = amqp.Connection(host='%s:%s' % (os.environ['RABBIT_MQ_HOST'],
                                               os.environ['RABBIT_MQ_PORT'],),
                               userid='%s' % os.environ['RABBIT_MQ_USER'],
                               password='%s' % os.environ['RABBIT_MQ_PASSWORD'],
                               virtual_host="/",
                               insist=False)

        chan = conn.channel()
        name, jobs, consumers = chan.queue_declare(queue=settings.CMSPYDER_DETECT_CMS_QUEUE,
                                                   passive=True)

        all_subdomains = Subdomains.objects.filter()
        subdomain_count = len(all_subdomains)

        all_scan_results = ScanResult.objects.filter()
        unique_scan_results = all_scan_results.values('subdomain').annotate(n=models.Count("pk"))
        unique_scan_results_count = len(unique_scan_results)

        unique_cms_results = all_scan_results.values('cms').annotate(n=models.Count("pk"))
        # can then get for each cms by making a filter


        # TODO rebuild index.html
