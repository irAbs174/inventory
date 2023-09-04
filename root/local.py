from pathlib import Path
import os


CSRF_TRUSTED_ORIGINS = ["https://8888-irabs174-inventory-n584xsmtszx.ws-eu104.gitpod.io",]

SECRET_KEY = 'django-insecure-qlxl!?s,dh>giuh&^%SALEDC98AD%^$AJHG!?><<ADadfAR*da'

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['8888-irabs174-inventory-n584xsmtszx.ws-eu104.gitpod.io']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# STATIC FILES (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',

    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# STATIC FILES DIRS
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Manifest Static Files Storage is recommended in production, to prevent outdated
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# static root Dir configuration
STATIC_ROOT = "/var/www/public/inventory/static"

# STATIC URL
STATIC_URL = '/static/'

# Media root Dir configuration
MEDIA_ROOT = "/var/www/public/inventory/media"

# Media URL
MEDIA_URL = 'media/'
