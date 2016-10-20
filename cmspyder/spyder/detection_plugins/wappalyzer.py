from base import BasePlugin
from spyder.models import ScanResult
from spyder.drivers.wappalyzer import WappalyzerDriver


class WappalyzerPlugin(BasePlugin):

    def __init__(self):
        super(WappalyzerPlugin, self).__init__()
        self.paths = ['/']
        self.wappalyzer_driver = WappalyzerDriver()


    def detect(self, subdomain, requests_results):
        if '/' in requests_results:
            results = self.wappalyzer_driver.analyze('http://%s/' % subdomain,  # TODO fix this?
                                                     requests_results['/'].text,
                                                     dict(requests_results['/'].headers))

            for r in results:
                if 'CMS' in results[r]['categories']:
                    ScanResult.objects.create(subdomain=subdomain,
                                              type=r.lower(),
                                              version=results[r]['version'] if
                                              results[r]['version'] else '')

