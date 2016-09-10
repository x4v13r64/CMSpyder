from wordpress import WordPressPlugin

detection_classes = [WordPressPlugin]

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
    plugins.append(_get_instance(WordPressPlugin))
    return plugins

