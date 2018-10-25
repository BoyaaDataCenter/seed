from threading import Thread

class BaseCache(Thread):
    prefix = "seed"

    def __init__(self, prefix=None):
        if not prefix:
            self.prefix = prefix

    def make_key(self, key):
        return '{}:{}'.format(
            self.prefix,
            key
        )

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, timeout):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
