import ast
# import third_party.PyV8_binaries.PyV8 as PyV8
from urllib.parse import urlparse
import json
import re
import warnings
import os
from bs4 import BeautifulSoup

from django.conf import settings


# class WappalyzerDriver(object):
#
#     def __init__(self):
#
#         f1 = open(os.path.join(settings.BASE_DIR,
#                                'third_party/Wappalyzer/src/wappalyzer.js'))
#         f2 = open(os.path.join(settings.BASE_DIR,
#                                'third_party/Wappalyzer/src/drivers/php/js/driver.js'))
#         f3 = open(os.path.join(settings.BASE_DIR,
#                                'third_party/Wappalyzer/src/apps.json'))
#
#         self.f_wappalyzer = f1.read()
#         f1.close()
#         self.f_driver = f2.read()
#         f2.close()
#         data = json.loads(f3.read())
#         f3.close()
#
#         self.apps = json.dumps(data['apps'])
#         self.categories = json.dumps(data['categories'])
#
#
#     def analyze(self, url, html, headers):
#
#         host = urlparse(url).hostname
#
#         data = {'host': host, 'url': url, 'html': html, 'headers': headers}
#
#         with PyV8.JSLocker():
#
#             context = PyV8.JSContext()
#
#             context.enter()
#
#             context.eval(self.f_wappalyzer)
#             context.eval(self.f_driver)
#
#             result = context.eval(
#                 "w.apps = %s; w.categories = %s; w.driver.data = %s; w.driver.init();"
#                 % (self.apps,
#                    self.categories,
#                    json.dumps(data)))
#
#             result_dict = ast.literal_eval(result)
#
#             context.leave()
#
#         return result_dict

# ---------------------------------------------------------------------------------------

__credit__ = "https://github.com/nemurici/python3-wappalyzer"

class WappalyzerDriver(object):
    """
    Python Wappalyzer driver.
    """

    def __init__(self):
        """
        Initialize a new Wappalyzer driver instance.
        """

        # load app and category definitions
        with open(os.path.join(settings.BASE_DIR, 'third_party/Wappalyzer/src/apps.json'), 'r') \
                as fd:
            apps_json = json.load(fd)

        self.categories = apps_json['categories']
        self.apps = apps_json['apps']

        for name, app in self.apps.items():
            self._prepare_app(app)

    def _prepare_app(self, app):
        """
        Normalize app data, preparing it for the detection phase.
        :param app:
        :return:
        """

        # Ensure these keys' values are lists
        for key in ['url', 'html', 'script', 'implies']:
            try:
                value = app[key]
            except KeyError:
                app[key] = []
            else:
                if not isinstance(value, list):
                    app[key] = [value]

        # Ensure these keys exist
        for key in ['headers', 'meta']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}

        # Ensure the 'meta' key is a dict
        obj = app['meta']
        if not isinstance(obj, dict):
            app['meta'] = {'generator': obj}

        # Ensure keys are lowercase
        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}

        # Prepare regular expression patterns
        for key in ['url', 'html', 'script']:
            app[key] = [self._prepare_pattern(pattern) for pattern in app[key]]

        for key in ['headers', 'meta']:
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = self._prepare_pattern(obj[name])

    def _prepare_pattern(self, pattern):
        """
        Strip out key:value pairs from the pattern and compile the regular
        expression.
        :param pattern:
        :return:
        """

        regex, _, rest = pattern.partition('\\;')
        try:
            return re.compile(regex, re.I)
        except re.error as e:
            warnings.warn(
                "Caught '{error}' compiling regex: {regex}"
                .format(error=e, regex=regex)
            )
            # regex that never matches:
            # http://stackoverflow.com/a/1845097/413622
            return re.compile(r'(?!x)x')

    def _has_app(self, app, url, headers, html, scripts, meta):
        """
        Determine whether the web page matches the app signature.
        :param app:
        :param url:
        :param headers:
        :param html:
        :param scripts:
        :param meta:
        :return:
        """

        # Search the easiest things first and save the full-text search of the HTML for last
        for regex in app['url']:
            if regex.search(url):
                return True
        for name, regex in app['headers'].items():
            if name in headers:
                content = headers[name]
                if regex.search(content):
                    return True

        for regex in app['script']:
            for script in scripts:
                if regex.search(script):
                    return True

        for name, regex in app['meta'].items():
            if name in meta:
                content = meta[name]
                if regex.search(content):
                    return True

        for regex in app['html']:
            if regex.search(html):
                return True

    def _get_implied_apps(self, detected_apps):
        """
        Get the set of apps implied by `detected_apps`.
        :param detected_apps:
        :return:
        """

        def __get_implied_apps(apps):
            _implied_apps = set()
            for app in apps:
                try:
                    _implied_apps.update(set(self.apps[app]['implies']))
                except KeyError:
                    pass
            return _implied_apps

        implied_apps = __get_implied_apps(detected_apps)
        all_implied_apps = set()

        # Descend recursively until we've found all implied apps
        while not all_implied_apps.issuperset(implied_apps):
            all_implied_apps.update(implied_apps)
            implied_apps = __get_implied_apps(all_implied_apps)

        return all_implied_apps

    def get_categories(self, app_name):
        """
        Returns a list of the categories for an app name.
        :param app_name:
        :return:
        """

        cat_nums = self.apps.get(app_name, {}).get("cats", [])
        cat_names = [self.categories.get("%s" % cat_num, "")
                     for cat_num in cat_nums]

        return cat_names

    def analyze(self, url, headers, html):
        """
        Analyze web page content.
        :param url:
        :param headers:
        :param html:
        :return:
        """

        # Parse the HTML with BeautifulSoup to find <script> and <meta> tags.
        parsed_html = BeautifulSoup(html, "html.parser")  # todo use lxml
        scripts = [script['src'] for script in parsed_html.findAll('script', src=True)]
        meta = {meta['name'].lower(): meta['content'] for meta in
                parsed_html.findAll('meta', attrs=dict(name=True, content=True))}

        detected_apps = set()

        for app_name, app in self.apps.items():
            if self._has_app(app, url, headers, html, scripts, meta):
                detected_apps.add(app_name)

        detected_apps |= self._get_implied_apps(detected_apps)

        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            categorised_apps[app_name] = {"categories": cat_names}

        return categorised_apps
