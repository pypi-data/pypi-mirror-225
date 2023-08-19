import os
import dj_database_url  # type: ignore
from typing import Any, Dict
from ..misc import resolve_environment


def resolve_database() -> Dict[str, str]:
    if resolve_environment() == "testing":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join("/tmp", "db.sqlite3"),
        }

    # Use unlimited persistent connections - https://docs.djangoproject.com/en/3.2/ref/databases/#persistent-connections
    return dj_database_url.config(conn_max_age=None)


def resolve_logging() -> Dict[str, Any]:
    if resolve_environment() == "testing":
        return {
            "version": 1,
            "root": {
                "level": "CRITICAL",  # Use a higher-level to disable logs in tests. Can't find a way to easily disable the root logger.
            },
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {  # Needed to prettify logs (especially for mini-huey/background task queue) to match gunicon logs format.
                "style": "{",
                "format": "[{asctime}] [{process}] [{levelname}] {message}",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }


def resolve_file_storage() -> str:
    if resolve_environment() == "testing":
        return "django.core.files.storage.InMemoryStorage"

    return "storages.backends.s3boto3.S3Boto3Storage"


def resolve_caches() -> Dict[str, Any]:
    if resolve_environment() == "testing":
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }

    return {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "django_cache",
        }
    }


BASE_INSTALLED_APPS = [
    "rest_framework",
    "django_filters",
    "vanoma_api_utils.mini_huey",
]

BASE_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "vanoma_api_utils.django.middlewares.CamelCaseMiddleWare",
]

BASE_REST_FRAMEWORK = {
    "ORDERING_PARAM": "sort",
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "vanoma_api_utils.rest_framework.renderers.CustomJsonRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "vanoma_api_utils.rest_framework.views.exception_handler",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "vanoma_api_utils.rest_framework.pagination.PageNumberPagination",
}

BASE_REST_FLEX_FIELDS = {
    "EXPAND_PARAM": "include",
    "OMIT_PARAM": "exclude",
}
