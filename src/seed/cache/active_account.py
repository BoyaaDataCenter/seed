import random
import string

from flask import current_app

from seed.cache.redis import RedisCache


class ActiveAccountCache(RedisCache):
    def __init__(self):
        self.redis_client = current_app.cache
        self.middle_key = 'active_account'

    def make_key(self, key):
        key = ":".join([self.middle_key, str(key)])
        return super(ActiveAccountCache, self).make_key(key)

    def create_active_token(self, user_id):
        active_token = ''.join([random.choice(string.ascii_lowercase + string.digits) for key in range(48)])
        self.set(active_token, user_id, timeout=24 * 60 * 60)
        return active_token

    def get_user_by_active_token(self, active_token):
        return self.get(active_token)
