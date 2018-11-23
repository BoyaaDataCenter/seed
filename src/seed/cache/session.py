import random
import string

from flask import current_app

from seed.cache.redis import RedisCache


class SessionCache(RedisCache):
    def __init__(self):
        self.redis_client = current_app.cache
        self.middle_key = 'session'

    def make_key(self, key):
        key = ':'.join([self.middle_key, str(key)])
        return super(SessionCache, self).make_key(key)

    def create_session(self, user_id):
        token = ''.join([random.choice(string.ascii_uppercase + string.digits) for key in range(32)])
        self.set(token, user_id, timeout=24 * 60 * 60)
        return token

    def get_user_id_by_token(self, token):
        return self.get(token)
