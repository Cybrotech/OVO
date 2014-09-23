"""
Django settings for ovo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = [
    ("Aashish Soni","aashish.soni@systematixindia.com")
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ghez38_woz84labuuleo)mmb@u&%4-b-2!q8ls3b^o_kt@6rf7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'my_user',
    'company',
    'website',
    'audience',
    'widget_tweaks',
    'south',
    'django_mailer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ovo.urls'

WSGI_APPLICATION = 'ovo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'ovo',
        'NAME': 'ovo.db',
        # 'USER': 'root',
        # 'PASSWORD': 'root',
        # 'HOST': '127.0.0.1',
        # 'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = "my_user.CustomUser"

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')

EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'

WEBSITE_NAME = "OVO"

DEFAULT_EMAIL_FROM_ADDRESS = "no-reply@ovo.com"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 # Replace with <mail server port>
EMAIL_HOST_USER = 'something@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True # Replace with True if TLS is required

STATIC_ROOT = os.path.join(BASE_DIR, "static").replace("\\","/")

MEDIA_ROOT = os.path.join(BASE_DIR, "../../media").replace("\\","/")

MEDIA_URL = '/media/'

from settings_local import *