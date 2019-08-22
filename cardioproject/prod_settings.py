from .settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()

DEBUG = False

TEMPLATE_DEBUG = False

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['sencardio.herokuapp.com']