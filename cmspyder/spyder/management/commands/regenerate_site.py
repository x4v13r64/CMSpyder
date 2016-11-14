import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from domains.models import Subdomain
from spyder.models import ScanResult


class Command(BaseCommand):
    help = 'Regenerate static website statistics'

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR, '../docs/index.html'), 'w') as index:

            index.write('<!DOCTYPE html>\n')
            index.write('<head>\n')
            index.write('<title>CMSpyder</title>\n')
            index.write('<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/'
                        'bootstrap/3.3.7/css/bootstrap.min.css\">\n')
            index.write('<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/'
                        'jquery.min.js\"></script>\n')
            index.write('</head>\n')
            index.write('<body>\n')
            index.write('<h1>CMSpyder</h1>')
            index.write('<p>A web crawler/scrapper with CMS detection '
                        '(<a href=\'https://github.com/j4v/CMSpyder\'>github.com/j4v/CMSpyder'
                        '</a>).</p>\n')

            index.write('<h2>General results</h2>\n')
            index.write('<ul>')
            index.write('<li>Domain count: {0!s}</li>\n'.format(Subdomain.objects.count()))

            index.write('<li>Domains analyzed: {0!s} ({1!s}% of all domains)</li>\n'
                        .format(Subdomain.objects.exclude(last_ip__isnull=True).count(),
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

            index.write('<h2>CMS detection results (click to expand)</h2>\n')
            index.write('<div class=\"list\">\n')
            for result_type in \
                    ScanResult.objects.filter().values('type').distinct().order_by('type'):
                index.write('<div>\n')
                index.write('<h3>{0!s}</h3>\n'.format(result_type['type']))

                scan_results_for_type = ScanResult.objects.filter(type=result_type['type'])

                index.write('<p>total count: {0!s} ({1!s}% of CMS detections)</p>\n'
                            .format(ScanResult.objects.filter(type=result_type['type']).
                                    values('subdomain').distinct().count(),
                                    ScanResult.objects.filter(type=result_type['type']).
                                    values('subdomain').distinct().count() *
                                    100/ScanResult.objects.filter().
                                    values('subdomain').distinct().count()))

                for version in \
                        scan_results_for_type.values('version').distinct().order_by('version'):
                    index.write('<ul hidden>\n')
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
                index.write('</div>\n')
            index.write('</div>\n')

            index.write('&lt;generated {0!s}&gt;\n'.format(timezone.now().
                        strftime("%Y-%m-%d %H:%M")))

            index.write('<script>\n')
            index.write('$(\'.list > div h3\').click(function() {\n')
            index.write('    $(this).parent().find(\'ul\').toggle();\n')
            index.write('});\n')
            index.write('</script>\n')

            index.write('</body>\n')
            index.write('</html>\n')
