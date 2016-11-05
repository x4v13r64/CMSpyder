from spyder.detection_plugins.wordpress import WordPressPlugin
from spyder.detection_plugins.drupal import DrupalPlugin
from spyder.detection_plugins.joomla import JoomlaPlugin
from spyder.detection_plugins.wappalyzer import WappalyzerPlugin

detection_classes = [WordPressPlugin, DrupalPlugin, JoomlaPlugin, WappalyzerPlugin]

_instances = {}
def _get_instance(cls):
    # Since some classes have non-trivial startup costs, keep instances around
    try:
        return _instances[cls]
    except KeyError:
        _instances[cls] = cls()
        return _instances[cls]

def get_detection_plugins():
    plugins = []
    # plugins.append(_get_instance(WordPressPlugin))
    # plugins.append(_get_instance(DrupalPlugin))
    # plugins.append(_get_instance(JoomlaPlugin))
    plugins.append(_get_instance(WappalyzerPlugin))
    return plugins

