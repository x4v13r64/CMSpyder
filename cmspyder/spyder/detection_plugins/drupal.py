import re

from spyder.detection_plugins.base import BasePlugin
from spyder.models import ScanResult


class DrupalPlugin(BasePlugin):

    def __init__(self):
        super(DrupalPlugin, self).__init__()
        self.paths = ['/']

    def detect(self, subdomain, requests_results):
        if '/' in requests_results and self._is_drupal(requests_results['/']):
                ScanResult.objects.create(subdomain=subdomain,
                                          type="drupal")

    def _is_drupal(self, request):

        for header in request.headers:
            if 'drupal' in header.lower() or 'drupal' in request.headers[header].lower():
                return True
        # if 'x-drupal-cache' in request.headers:
        #     return True
        # if 'x-xenerator' in request.headers and 'Drupal' in request.headers['x-generator']:
        #     return True
        #     # x_generator_regex = 'Drupal(?:\\s([\\d.]+))?\\;version:\\1"'
        #     # p = re.compile(x_generator_regex)
        #     # result = p.search(request.headers['X-Generator'])
        #     # if result:
        #     #     return True
        # else:
        #     return False
        #
        #     # p = re.compile('<(?:link|style)[^>]+sites(?:default|all)(?:themes|modules)')
        #     # result = p.search(html)
        #     # return result
