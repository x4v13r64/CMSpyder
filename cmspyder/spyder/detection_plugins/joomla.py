from base import BasePlugin
from spyder.models import ScanResult

import re


class JoomlaPlugin(BasePlugin):

    def __init__(self):
        super(JoomlaPlugin, self).__init__()
        self.paths = ['/']

    def detect(self, subdomain, requests_results):
        if '/' in requests_results:
            if self._is_joomla(requests_results['/']):
                ScanResult.objects.create(subdomain=subdomain,
                                          type="joomla")

    def _is_joomla(self, request):

        for header in request.headers:
            if 'joomla' in header.lower() or 'joomla' in request.headers[header].lower():
                return True

