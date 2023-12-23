from .local import *


INSTALLED_APPS = [
    "ash",
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'import_export',
    "dashboard",
    "account",
    "inventory",
    "orders",
    "chat",
]
# LOGIN REDIRECT URL
LOGIN_REDIRECT_URL = '/'

SESSION_EXPIRE_SECONDS = 1500

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_TIMEOUT_REDIRECT = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE=True

AUTHENTICATION_BACKENDS = [
    'account.backend.EmailPhoneCodeMelliBackend',
]

# REST FRAMEWORK CONF
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 30,
    'MARGIN_PAGES_DISPLAYED': 6,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

AUTH_USER_MODEL = "account.user_accounts"

AUTH_USER_MODEL_USER_PERMISSIONS_RELATIONSHIP = "custom_user_permissions"

AUTHENTICATIONS_BACKENDS = [
    "account.backend.Authenticate",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "template")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.accuonts_list",
            ],
        },
    },
]

WSGI_APPLICATION = "root.wsgi.application"

ASGI_APPLICATION = "root.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
