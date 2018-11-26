from flask import current_app
from seed.cache.active_account import ActiveAccountCache


class ResetPasswordCache(ActiveAccountCache):
    def __init__(self):
        self.redis_client = current_app.cache
        self.middle_key = 'reset_password'
