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
            index.write('<li>Domains fingerprinted: %s (%s%% of all domains)</li>\n' %
                        (ScanResult.objects.values('subdomain').distinct().count(),
                         ScanResult.objects.values('subdomain').distinct().count() *
                         100/Subdomain.objects.count()))
            index.write('</ul>\n')

            index.write('<h2>CMS detection results</h2>\n')
            # TODO these stats are incorrect as they aren't for unique detections
            index.write('<ul id="result_tree">\n')
            for result_type in \
                    ScanResult.objects.filter().values('type').distinct().order_by('type'):
                index.write('<li><span>%s</span></li>\n' % result_type['type'])

                scan_results_for_type = ScanResult.objects.filter(type=result_type['type'])

                index.write('<ul>\n')
                index.write('<li><span>total count: %s (%s%% of CMS detections)</span></li>\n' %
                            (ScanResult.objects.filter(type=result_type['type']).count(),
                             ScanResult.objects.filter(type=result_type['type']).count() *
                             100/ScanResult.objects.count()))

                for version in \
                        scan_results_for_type.values('version').distinct().order_by('version'):
                    index.write('<ul>\n')
                    index.write('<li><span>version \'%s\' count: %s '
                                '(%s%% of %s detections)</span></li>\n' %
                                (version['version'] if version['version'] else 'unknown',
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).count(),
                                 ScanResult.objects.filter(type=result_type['type'],
                                                           version=version['version']).count() *
                                 100/ScanResult.objects.filter(type=result_type['type']).count(),
                                 result_type['type']))
                    index.write('</ul>\n')

                index.write('</ul>\n')
            index.write('</ul>\n')

            index.write('&lt;generated %s&gt;\n' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

            index.write('<script src=\"http://code.jquery.com/jquery-1.10.1.min.js\"></script>\n<script type=\"text/javascript\">$(function(){$(\'#result_tree\').find(\'span\').click(function(e){$(this).parent().children(\'ul\').toggle();});});</script>\n')

            # index.write('<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>')
            # index.write('<script type="text/javascript">')
            # index.write('$(\'#tree\').find(\'span\').click(function(e){$(this).parent().'
            #             'children(\'ul\').toggle();});')
            # # index.write('$(\'.tree\').find(\'span\').parent().children(\'ul\').hide();')
            # index.write('</script>')

            index.write('</html>\n')
