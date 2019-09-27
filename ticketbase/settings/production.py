import sentry_sdk
import dj_database_url
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

sentry_sdk.init(
    integrations=[DjangoIntegration()],
    environment='production',
)
