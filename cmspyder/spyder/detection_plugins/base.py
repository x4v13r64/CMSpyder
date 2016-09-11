class BasePlugin(object):

    def __init__(self):
        self.paths = ['/']

    def detect(self, subdomain, request):
        raise NotImplementedError
