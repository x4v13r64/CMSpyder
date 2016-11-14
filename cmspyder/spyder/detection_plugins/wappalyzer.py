from spyder.detection_plugins.base import BasePlugin
from spyder.drivers.wappalyzer import WappalyzerDriver
from spyder.models import ScanResult
from distutils.version import LooseVersion


class WappalyzerPlugin(BasePlugin):

    def __init__(self):
        super(WappalyzerPlugin, self).__init__()
        self.paths = ['/']
        self.wappalyzer_driver = WappalyzerDriver()


    def detect(self, subdomain, requests_results):
        if '/' in requests_results:
            results = self.wappalyzer_driver.analyze('http://%s/' % subdomain,
                                                     dict(requests_results['/'].headers),
                                                     requests_results['/'].text)

            for r in results:
                if 'CMS' in results[r]['categories']:

                    # find greatest version
                    if len(results[r]['versions']) > 1:
                        greatest_version = results[r]['versions'][0]
                        for v in results[r]['versions']:
                            if LooseVersion(v) > LooseVersion(greatest_version):
                                greatest_version = v
                        version = 1
                    elif len(results[r]['versions']) == 1:
                        version = results[r]['versions'][0]
                    else:
                        version = None

                    ScanResult.objects.create(subdomain=subdomain,
                                              type=r.lower(),
                                              version=version if version else '')
