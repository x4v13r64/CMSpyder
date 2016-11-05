import ast
import json
import os
import third_party.PyV8_binaries.PyV8 as PyV8
from urllib.parse import urlparse

from django.conf import settings


class WappalyzerDriver(object):

    def __init__(self):

        f1 = open(os.path.join(settings.BASE_DIR,
                               'third_party/Wappalyzer/src/wappalyzer.js'))
        f2 = open(os.path.join(settings.BASE_DIR,
                               'third_party/Wappalyzer/src/drivers/php/js/driver.js'))
        f3 = open(os.path.join(settings.BASE_DIR,
                               'third_party/Wappalyzer/src/apps.json'))

        self.f_wappalyzer = f1.read()
        f1.close()
        self.f_driver = f2.read()
        f2.close()
        data = json.loads(f3.read())
        f3.close()

        self.apps = json.dumps(data['apps'])
        self.categories = json.dumps(data['categories'])


    def analyze(self, url, html, headers):

        host = urlparse(url).hostname

        data = {'host': host, 'url': url, 'html': html, 'headers': headers}

        with PyV8.JSLocker():

            context = PyV8.JSContext()

            context.enter()

            context.eval(self.f_wappalyzer)
            context.eval(self.f_driver)

            result = context.eval(
                "w.apps = %s; w.categories = %s; w.driver.data = %s; w.driver.init();"
                % (self.apps,
                   self.categories,
                   json.dumps(data)))

            result_dict = ast.literal_eval(result)

            context.leave()

        return result_dict
