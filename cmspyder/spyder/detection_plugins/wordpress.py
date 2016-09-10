import requests
from bs4 import BeautifulSoup
from django.conf import settings

from base import BasePlugin
from spyder.models import ScanResult


class WordPressPlugin(BasePlugin):

    def detect(self, subdomain, request):
        soup = BeautifulSoup(request.text)
        if self._is_wordpress(soup):
            scan_result = ScanResult.objects.create(subdomain=subdomain,
                                                    type="wordpress")


    def _is_wordpress(self, soup):
        meta_tags = soup.find_all('meta', {'name': 'generator'})

        for meta_tag in meta_tags:
            if meta_tag['content'].lower().startswith('wordpress'):
                return True

        css_tags = soup.find_all('link', rel='stylesheet')
        for css_tag in css_tags:
            try:
                if 'wp-content' in css_tag['href'] or 'wp-include' in css_tag['href']:
                    return True
            except Exception, e:
                # Some tags don't have `href`
                pass

        script_tags = soup.find_all('script')
        for script_tag in script_tags:
            try:
                if 'wp-content' in script_tag['src'] or 'wp-include' in script_tag['src']:
                    return True
            except Exception, e:
                # Some tags don't have `src`
                pass

        return False
