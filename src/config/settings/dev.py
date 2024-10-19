from config.settings.base import *  # NOQA

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-280gtlp9=+j3h%!1z0n_pi!f=@!-1(!aix58@gq&c&zh3_m4=0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += []  # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # NOQA
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
