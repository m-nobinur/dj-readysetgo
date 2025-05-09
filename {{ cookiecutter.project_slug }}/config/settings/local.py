# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import env

# =============================
# GENERAL DEV CONFIGURATION
# =============================
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="oh7zRMUPkDmWw2bf99zIpoLMXT4FPnxiHiO1tOuYqMwQNLf50y4wnwCBheQnA2JP",
)

# =============================
# HOST CONFIGURATION
# =============================
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104

# =============================
# CACHES CONFIGURATION
# =============================
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# =============================
# MAILPIT CONFIGURATION
# =============================
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# =============================
# DEBUG TOOLBAR CONFIGURATION
# =============================
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# =============================
# DJANGO EXTENSIONS CONFIG
# =============================
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]

# =============================
# CELERY CONFIG
# =============================
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ==============================================================
# django-allauth development config
# ==============================================================
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "EMAIL_AUTHENTICATION": True,
        "APPS": [
            {
                "client_id": env.str("GOOGLE_CLIENT_ID", default="OHzTtJV0nEvyyBi3"),
                "secret": env.str("GOOGLE_SECRET", default="OHzTtJV0nEvyyBi3xx"),
                "key": "",
            },
        ],
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}
