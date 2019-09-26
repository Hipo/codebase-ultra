import redis
from .base import *

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'test',
        'HOST': 'postgres_testing',
        'PORT': '5432',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

REDIS_HOST = 'redis_testing'
REDIS_PORT = 6379
REDIS_CELERY_NUMBER = 1
REDIS_CONNECTION = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=3)
CELERY_BROKER_URL = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, REDIS_CELERY_NUMBER)
CELERY_RESULT_BACKEND = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, REDIS_CELERY_NUMBER + 1)