import json
import os
import re
import warnings

from bs4 import BeautifulSoup
from django.conf import settings

__credit__ = "https://github.com/scrapinghub/wappalyzer-python"


class Pattern(object):
    """
    Each pattern in the apps.json file will be kept as an object, who stores the compiled regex
    as well as if the regex returns a version.
    """

    def __init__(self, pattern):
        """

        :param pattern:
        :param has_version:
        """

        regex, _, rest = pattern.partition('\\;')

        try:
            self.regex = re.compile(regex, re.I)
            self.has_version = 'version' in rest  # todo improve version detection
        except re.error as e:
            warnings.warn("Caught '{error}' compiling regex: {regex}".format(error=e, regex=regex))
            self.pattern = None


class WappalyzerDriver(object):
    """
    Python Wappalyzer driver.
    """

    # todo detect versions that are not of type \1:
    """
    version:\1
    version:\1?\1:\2
    version:\1 \2
    version:\1?4.1+:
    version:2
    version:2
    version:\1?Enterprise:Community
    confidence:50\;version:2
    version:\1.\2.\3
    version:API v\1
    version:\1?4:5
    version:2+
    version:\1?2+:
    version:\1?\1:\2
    """
    # todo also detect "confidence"
    # todo also regex 'env'

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

        # Ensure keys' values are lists
        for key in ['url', 'html', 'script', 'implies']:
            try:
                value = app[key]
            except KeyError:
                app[key] = []
            else:
                if not isinstance(value, list):
                    app[key] = [value]

        # Ensure keys exist
        for key in ['headers', 'meta']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}

        # Ensure 'meta' key is a dict
        obj = app['meta']
        if not isinstance(obj, dict):
            app['meta'] = {'generator': obj}

        # Ensure keys are lowercase
        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}

        # Prepare regular expression patterns
        for key in ['url', 'html', 'script']:
            app[key] = [Pattern(pattern) for pattern in app[key]]

        for key in ['headers', 'meta']:
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = Pattern(obj[name])

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

        found = False
        versions = set()

        for pattern in app['url']:
            if pattern.regex and pattern.regex.search(url):
                # detected
                found = True
                # find version
                if pattern.has_version:
                    versions.update(pattern.regex.search(url).group(1))

        for name, pattern in app['headers'].items():
            if name.lower() in headers:
                content = headers[name.lower()]
                if pattern.regex and pattern.regex.search(content):
                    # detected
                    found = True
                    # find version
                    if pattern.has_version:
                        version = pattern.regex.search(content).group(1)
                        if version:
                            versions.update(version)

        for pattern in app['script']:
            for script in scripts:
                if pattern.regex and pattern.regex.search(script):
                    # detected
                    found = True
                    # find version
                    if pattern.has_version:
                        version = pattern.regex.search(script).group(1)
                        if version:
                            versions.update(version)

        for name, pattern in app['meta'].items():
            if name.lower() in meta:
                content = meta[name]
                if pattern.regex and pattern.regex.search(content):
                    # detected
                    found = True
                    # find version
                    if pattern.has_version:
                        version = pattern.regex.search(content).group(1)
                        if version:
                            versions.update(version)

        for pattern in app['html']:
            if pattern.regex and pattern.regex.search(html):
                # detected
                found = True
                # find version
                if pattern.has_version:
                    version = pattern.regex.search(html).group(1)
                    if version:
                        versions.update(version)

        return found, versions

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
        # make all headers lowercase
        headers_lower = {h.lower(): v for h, v in headers.items()}

        detected_apps = dict()

        for app_name, app in self.apps.items():
            has_app, versions = self._has_app(app, url, headers_lower, html, scripts, meta)
            if has_app:
                if app_name in detected_apps:
                    detected_apps[app_name] |= versions
                else:
                    detected_apps[app_name] = versions

        # todo support the get_implied_apps method
        # dict not compatible with set
        # detected_apps |= self._get_implied_apps(detected_apps)  # merge set

        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            categorised_apps[app_name] = {"categories": cat_names,
                                          "versions": list(detected_apps[app_name])}

        return categorised_apps
