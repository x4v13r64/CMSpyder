class BasePlugin(object):

    def detect(self, subdomain, request):
        raise NotImplementedError
