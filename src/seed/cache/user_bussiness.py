from flask import current_app

from seed.cache.redis import RedisCache


class UserBussinessCache(RedisCache):
    def __init__(self):
        self.redis_client = current_app.cache
        self.middle_key = 'user_bussiness'

    def make_key(self, key):
        key = ':'.join([self.middle_key, str(key)])
        return super(UserBussinessCache, self).make_key(key)