import os

from django.apps import apps

from hogwarts.magic_templates.gen_templates import Endpoint, get_endpoint, ViewType
from hogwarts.magic_urls.gen_urls import get_app_name
from hogwarts.magic_urls.utils import extract_paths
from hogwarts.views import ExampleCreateView


def test_it_gets_endpoint():
    base_path = apps.get_app_config("hogwarts").path
    urls_code = open(os.path.join(base_path, "urls.py"), "r").read()

    paths = extract_paths(urls_code)
    app_name = get_app_name(urls_code)

    endpoint = get_endpoint(ExampleCreateView, paths, app_name)

    expected = Endpoint(
        view=ExampleCreateView,
        template_name=ExampleCreateView.template_name,
        path_name="example:create",
        view_type=ViewType.CREATE,
        model=ExampleCreateView.model
    )

    assert endpoint == expected
