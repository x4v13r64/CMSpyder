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

            index.write('<html>\n')

            index.write('<h1>CMSpyder</h1>')
            index.write('<p>A web crawler/scrapper with CMS detection '
                        '(<a href=\'https://github.com/j4v/CMSpyder\'>github.com/j4v/CMSpyder'
                        '</a>).</p>\n')

            index.write('<h2>General statistics</h2>\n')
            index.write('<ul>')
            index.write('<li>Domain count: %s</li>\n' % Subdomain.objects.count())

            index.write('<li>Domains analyzed: %s (%s%% of all domains)</li>\n' %
                        (Subdomain.objects.exclude(last_ip__isnull=True).count(),
                         Subdomain.objects.exclude(last_ip__isnull=True).count() *
                         100/Subdomain.objects.count()))
            index.write('<li>Domains fingerprinted: %s (%s%% of all domains & %s%% of '
                        'analyzed domains)</li>\n' %
                        (ScanResult.objects.values('subdomain').distinct().count(),
                         ScanResult.objects.values('subdomain').distinct().count() *
                         100/Subdomain.objects.count(),
                         ScanResult.objects.values('subdomain').distinct().count() *
                         100/Subdomain.objects.exclude(last_ip__isnull=True).count()))
            index.write('</ul>\n')

            index.write('<h2>CMS detection results</h2>\n')
            for result_type in \
                    ScanResult.objects.filter().values('type').distinct().order_by('type'):
                index.write('<h3>%s</h3>\n' % result_type['type'])

                scan_results_for_type = ScanResult.objects.filter(type=result_type['type'])

                index.write('<ul>\n')
                index.write('<li>total count: %s (%s%% of CMS detections)</li>\n' %
                            (ScanResult.objects.filter(type=result_type['type']).
                             values('subdomain').distinct().count(),
                             ScanResult.objects.filter(type=result_type['type']).
                             values('subdomain').distinct().count() *
                             100/ScanResult.objects.filter().
                             values('subdomain').distinct().count()))

                for version in \
                        scan_results_for_type.values('version').distinct().order_by('version'):
                    index.write('<ul>\n')
                    index.write('<li>version \'%s\' count: %s '
                                '(%s%% of %s detections)</li>\n' %
                                (version['version'] if version['version'] else 'unknown',
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).
                                 values('subdomain').distinct().count(),
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).
                                 values('subdomain').distinct().count() *
                                 100/ScanResult.objects.filter(type=result_type['type']).
                                 values('subdomain').distinct().count(),
                                 result_type['type']))
                    index.write('</ul>\n')

                index.write('</ul>\n')

            index.write('&lt;generated %s&gt;\n' % datetime.datetime.now().
                        strftime("%Y-%m-%d %H:%M"))

            index.write('</html>\n')
