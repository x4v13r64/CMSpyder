import os
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from domains.models import Subdomain
from spyder.models import ScanResult


class Command(BaseCommand):
    help = 'Regenerate static website statistics'

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR, '../docs/index.html'), 'w') as index:

            index.write('<html>')
            index.write('<h1>CMSpyder</h1>')
            index.write('<p>A web crawler/scrapper with CMS detection '
                        '(<a href=\'https://github.com/j4v/CMSpyder\'>github.com/j4v/CMSpyder'
                        '</a>).</p>')

            index.write('<h2>General statistics</h2>')
            index.write('<ul>')
            index.write('<li>Domain count: %s</li>' % Subdomain.objects.count())

            scan_results = ScanResult.objects.filter()
            index.write('<li>Unique domains analyzed: %s</li>' %
                        scan_results.values('subdomain').distinct().count())
            index.write('<li>Analysis count: %s</li>' % ScanResult.objects.count())
            index.write('</ul>')

            index.write('<h2>CMS detection results</h2>')
            # TODO these stats are incorrect as they aren't for unique detections
            for result_type in scan_results.values('type').distinct():
                index.write('<h3>%s</h3>' % result_type['type'])

                scan_results_for_type = ScanResult.objects.filter(type=result_type['type'])

                index.write('<ul>')
                index.write('<li>total count: %s (%s%% of CMS detections)</li>' %
                            (ScanResult.objects.filter(type=result_type['type']).count(),
                             ScanResult.objects.filter(type=result_type['type']).count() *
                             100/ScanResult.objects.count()))

                for version in scan_results_for_type.values('version').distinct():
                    index.write('<ul>')
                    index.write('<li>version \'%s\' count: %s (%s%% of %s detections)</li>' %
                                (version['version'] if version['version'] else 'unknown',
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).count(),
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).count() *
                                 100/ScanResult.objects.filter(type=result_type['type']).count(),
                                 result_type['type']))
                    index.write('</ul>')

                index.write('</ul>')

            index.write('&lt;generated %s&gt;' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            index.write('</html>')
