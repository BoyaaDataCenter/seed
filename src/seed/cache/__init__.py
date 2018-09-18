from flask import current_app

from seed.cache.redis import RedisCache

__all__ = ['DefaultCache']

DefaultCache = RedisCache