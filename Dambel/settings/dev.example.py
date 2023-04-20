# create dev.py in current directory and copy the below code

from .common import *

SECRET_KEY = 'your-secret-key'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER ': 'db_user',
        'PASSWORD': 'db_pass',
        'HOST': 'localhost',
    }
}

STATIC_ROOT = 'static'
