from .common import *
import os

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split()
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER ': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('HOST'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
