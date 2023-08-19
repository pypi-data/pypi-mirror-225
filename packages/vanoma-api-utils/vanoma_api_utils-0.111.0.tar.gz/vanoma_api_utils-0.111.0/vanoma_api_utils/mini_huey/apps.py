from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ApiConfig(AppConfig):
    name = "vanoma_api_utils.mini_huey"

    def ready(self) -> None:
        # Discover all background so that they can be scheduled
        autodiscover_modules("background")
