import json
from typing import Any, Dict
from django.apps import apps
from django.core.files.base import ContentFile
from pathlib import Path


def load_fixture_as_json(name: str) -> Dict[str, Any]:
    for app_config in apps.get_app_configs():
        file_path = f"{app_config.path}/fixtures/{name}"
        if Path(file_path).exists():
            with open(file_path, "r") as rfile:
                return json.load(rfile)

    raise Exception(f"Fixuture {name} not found.")


def load_fixture_as_binary(name: str) -> bytes:
    for app_config in apps.get_app_configs():
        file_path = f"{app_config.path}/fixtures/{name}"
        if Path(file_path).exists():
            with open(file_path, "rb") as rfile:
                return rfile.read()

    raise Exception(f"Fixture file {name} not found.")


def load_fixture_as_content_file(name: str) -> ContentFile:
    _bytes = load_fixture_as_binary(name)
    return ContentFile(_bytes, name=name)
