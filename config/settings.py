from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", True)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
]
THIRD_PARTY_APPS = [
    "rest_framework",
]

LOCAL_APPS = [
    "test_app",
    "another_app",
    "automatic_rest"
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="m0veGl8I8wLxOf6T21ZkGfthB3wQ8okiszsSdT4VYXh6c3rylClq37zcpbNJSAvE",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'PAGE_SIZE': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'ORDERING_PARAM': 'order_by',
}
