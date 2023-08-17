import importlib

from django.core.management.base import CommandError
from django.apps import apps


def get_app_config(app_name: str):
    try:
        return apps.get_app_config(app_name)
    except LookupError:
        raise CommandError(f"App '{app_name}' does not exist.")


def get_views_module(app_name: str):
    try:
        # Import the views.py file dynamically
        return importlib.import_module(f"{app_name}.views")
    except ModuleNotFoundError:
        raise CommandError(f"Views not found for app '{app_name}'.")
