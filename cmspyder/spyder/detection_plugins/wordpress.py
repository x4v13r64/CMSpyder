from bs4 import BeautifulSoup

from base import BasePlugin
from spyder.models import ScanResult


class WordPressPlugin(BasePlugin):

    def __init__(self):
        super(WordPressPlugin, self).__init__()
        self.paths = ['/']

    def detect(self, subdomain, requests_results):
        if '/' in requests_results:
            soup = BeautifulSoup(requests_results['/'].text)
            if self._is_wordpress(soup):
                ScanResult.objects.create(subdomain=subdomain,
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
            # Some tags don't have `href`
            except Exception, e:
                pass

        script_tags = soup.find_all('script')
        for script_tag in script_tags:
            try:
                if 'wp-content' in script_tag['src'] or 'wp-include' in script_tag['src']:
                    return True
            # Some tags don't have `src`
            except Exception, e:
                pass

        return False
