import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']


# Database credential LOCAL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moveCollection',
        'USER': 'root',
        'PASSWORD': 'PWD',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}


# Static assets
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static_dirs'),
)# User uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')