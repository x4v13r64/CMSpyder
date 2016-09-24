class BasePlugin(object):

    def __init__(self):
        self.paths = ['/']

    def detect(self, subdomain, requests_results):
        raise NotImplementedError
