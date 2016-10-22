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
            subdomains = Subdomain.objects.filter()
            index.write('<li>Domain count: %s</li>' % len(subdomains))

            scan_results = ScanResult.objects.filter()
            scan_results_unique_subdomain = scan_results.values('subdomain').distinct()
            index.write('<li>Unique domains analyzed: %s</li>' % len(scan_results_unique_subdomain))
            index.write('<li>Analysis count: %s</li>' % len(scan_results))
            index.write('</ul>')

            index.write('<h2>CMS detection results</h2>')
            unique_scan_results = scan_results.values('type').distinct()

            # TODO these stats are incorrect as they aren't for unique detections
            for result_type in unique_scan_results:
                index.write('<h3>%s</h3>' % result_type['type'])

                scan_results_for_type = scan_results.filter(type=result_type['type'])

                index.write('<ul>')
                index.write('<li>total count: %s (%s%% of CMS detections)</li>' %
                            (len(scan_results_for_type),
                             len(scan_results_for_type)*100/len(scan_results)))

                scan_results_versions_for_type = \
                    scan_results_for_type.values('version').distinct()

                for version in scan_results_versions_for_type:
                    index.write('<ul>')
                    scan_results_versions_for_type_version = \
                        ScanResult.objects.filter(type=result_type['type'],
                                                  version=version['version'])
                    index.write('<li>version \'%s\' count: %s (%s%% of %s detections)</li>' %
                                (version['version'] if version['version'] else 'unknown',
                                 len(scan_results_versions_for_type_version),
                                 len(scan_results_versions_for_type_version) *
                                 100/len(scan_results_for_type),
                                 result_type['type']))
                    index.write('</ul>')

                index.write('</ul>')

            index.write('&lt;generated %s&gt;' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            index.write('</html>')
