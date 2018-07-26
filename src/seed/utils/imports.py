

class ModelProxyCache(dict):
    def __missing__(self, path):
        if '.' not in path:
            return __import__(path)

        module_name, class_name = path.rsplit('.', 1)

        module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(module, class_name)

        self[path] = handler
        return handler


_cache = ModelProxyCache()


def import_string(path):
    """ Path must be models.path.ClassName
    """
    result = _cache[path]
    return result
