"""
seed.conf.server
~~~~~~~~~~~~~~~~

There setting act as default(base) settings for the seed-provided web-server
"""

import os

ENVRIOMENT = os.environ.get('SEED_ENVRIOMENT', 'production')

IS_DEV = ENVRIOMENT == 'development'

DEBUG = IS_DEV

# Seed logs formatting
LOGGING = {
    'default_level': 'INFO',
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
}