import json

from seed.cache.base import BaseCache


class RedisCache(BaseCache):
    max_size = 50 * 1024 * 1024

    def __init__(self, redis):
        self.redis_client = redis

    def set(self, key, value, timeout=None):
        key = self.make_key(key)
        v = json.dumps(value)
        if len(v) > self.max_size:
            raise ValueError("Cache value too large: %r %r" %(key, len(value)))
        if timeout:
            self.redis_client.set(key, v, int(timeout))
        else:
            self.redis_client.set(key, v)

    def get(self, key):
        key = self.make_key(key)
        result = self.redis_client.get(key)
        if result:
            result = json.loads(result)
        return result

    def delete(self, key):
        key = self.make_key(key)
        self.redis_client.delete(key)