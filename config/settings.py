"""
Django settings for config project.
"""

# Libraries
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(
    env.path(
        "ENV_FILE_PATH",
        default=(environ.Path(__file__)-2).path(".env")()
    )()
)

# Build paths inside the project like this: BASE_DIR / "subdir".


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]


# Application definition

USER_APPLICATIONS = [
    "pages.apps.PagesConfig",
    "accounts.apps.AccountsConfig",
    "todos.apps.TodosConfig",
    "socials.apps.SocialsConfig",
    "manga_anime.apps.MangaAnimeConfig",
    "to_buy.apps.ToBuyConfig",
    "products.apps.ProductsConfig",
    "stores.apps.StoresConfig",
    "cash_flow.apps.CashFlowConfig",
    "library.apps.LibraryConfig",
]

EXTERNALS_APPLICATIONS = [
    "django.contrib.gis",
    "versatileimagefield",
    "colorfield",
    "location_field.apps.DefaultConfig",
    "djmoney",
    "django_filters",
    "pwa",
    "django_celery_results",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
] + USER_APPLICATIONS + EXTERNALS_APPLICATIONS

MIDDLEWARE = [
    # "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, 'django_admin_geomap', 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


MODE = env("MODE", default="test")
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env("DATABASE_NAME"),
            'USER': env("DATABASE_USER"),
            'PASSWORD': env("DATABASE_PASSWORD"),
            'HOST': env("DATABASE_HOST"),
            'PORT': env("DATABASE_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
DEFAULT_HASHING_ALGORITHM="sha1"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Static Configuration
STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, "static/"),
)

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "static/js", "serviceworker.js")

# Redirect when i can load
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "pages:home"
LOGOUT_REDIRECT_URL = "pages:home"


# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static Settings
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Spotify connect
SPOTIFY_CLIENT_ID = env("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = env("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = env("SPOTIFY_REDIRECT_URI")

# Pagination
PAGINATION_LIMIT = 10

# Telegram Connection
TELEGRAM_API_ID = env("TELEGRAM_API_ID")
TELEGRAM_API_HASH = env("TELEGRAM_API_HASH")
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
PHONE_DEFAULT = "+573057882366"

# Location
LOCATION_FIELD_PATH = STATIC_URL + 'location_field'

LOCATION_FIELD = {
    'map.provider': 'openstreetmap',
    'search.provider': 'nominatim',

    'resources.root_path': LOCATION_FIELD_PATH,
    'resources.media': {
        'js': (
            LOCATION_FIELD_PATH + '/js/form.js',
        ),
    },
}
INITIAL_LOCATION: list[float] = [4.599011638118746, -74.08252716064453]

DEFAULT_CURRENCIES: list[str] = [
    "COP",
    "USD",
    "CAD"
]

# PWA
PWA_APP_NAME = "Smart Home DG"
PWA_APP_DESCRIPTION = "Smart Home DG"
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {
        "src": "static/imgs/brands/house-160.png",
        "sizes": "160x160"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "static/imgs/brands/house-160.png",
        "sizes": "160x160"
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "static/imgs/brands/house-160.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)"
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"

# Celery Configuration Options
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_TIMEZONE = "America/Bogota"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Configuration of Sending of Email
EMAIL_PROVIDER = "django_email"
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# BOOkS
BOOK_SEND_EMAIL_SUBJECT = "Smart Home Sync Send Book"
BOOK_SEND_EMAIL_BODY = "The current content is sended based Smart Home DyG"
PATH_BOOKS = BASE_DIR / "media" / "books"