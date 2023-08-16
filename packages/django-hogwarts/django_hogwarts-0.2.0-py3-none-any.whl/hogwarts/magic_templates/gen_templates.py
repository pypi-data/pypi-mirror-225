import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Union

from jinja2 import Environment
from django.views.generic import DetailView, CreateView
from django.conf import settings
from django.db.models import Model
from django.apps import apps

from hogwarts.magic_urls._base import import_views
from hogwarts.magic_urls.utils import Path, extract_paths
from hogwarts.management.commands.base import get_views_module

GENERIC_VIEWS = ("CreateView", "UpdateView", "ListView", "DetailView")

SCAFFOLD_FOLDER = os.path.join(apps.get_app_config("hogwarts").path, "scaffold")
TEMPLATES_FOLDER = settings.TEMPLATES[0]["DIRS"][0]
env = Environment("[#", "#]", "[[", "]]")


class ViewType(Enum):
    CREATE = "CreateView"
    UPDATE = "UpdateView"
    DETAIL = "DetailView"
    LIST = "ListView"


@dataclass
class Endpoint:
    view: Union[DetailView, CreateView]
    template_name: str
    path_name: str
    model: Type[Model]
    view_type: Optional[ViewType]


def gen_templates(app_name: str):
    endpoints = get_endpoints(app_name)

    for endpoint in endpoints:
        fields = [field.name for field in endpoint.model._meta.fields]
        model_name = endpoint.model.__name__

        if endpoint.view_type == ViewType.CREATE:
            result = render_template({"model": model_name}, "create")
            write_template(endpoint.template_name, result)
            print("created template:", endpoint.template_name)

        elif endpoint.view_type == ViewType.UPDATE:
            result = render_template({"model": model_name}, "update")
            write_template(endpoint.template_name, result)
            print("created template:", endpoint.template_name)


        elif endpoint.view_type == ViewType.LIST:
            name = endpoint.view.context_object_name
            create_path_name = find_path_name(endpoints, endpoint.model, ViewType.CREATE)
            detail_path_name = find_path_name(endpoints, endpoint.model, ViewType.DETAIL)

            context_data = {
                "fields": fields,
                "item": name[:-1],
                "items": name,
                "create_path_name": create_path_name,
                "detail_path_name": detail_path_name
            }

            result = render_template(context_data, "list")
            write_template(endpoint.template_name, result)
            print("created template:", endpoint.template_name)

        elif endpoint.view_type == ViewType.DETAIL:
            name = endpoint.view.context_object_name
            update_path_name = find_path_name(endpoints, endpoint.model, ViewType.UPDATE)
            list_path_name = find_path_name(endpoints, endpoint.model, ViewType.LIST)
            context_data = {
                "fields": fields,
                "item": name,
                "list_path_name": list_path_name,
                "update_path_name": update_path_name
            }

            result = render_template(context_data, "detail")
            write_template(endpoint.template_name, result)
            print("created template:", endpoint.template_name)


def find_path_name(endpoints: list[Endpoint], model, view_type: ViewType):
    for endpoint in endpoints:
        if endpoint.model == model and endpoint.view_type == view_type:
            return endpoint.path_name

    return None


def render_template(context_data: dict, action):
    create = open(os.path.join(SCAFFOLD_FOLDER, f"{action}.html"), "r").read()
    template = env.from_string(create)
    return template.render(context_data)


def write_template(template_path, content):
    full_path = os.path.join(TEMPLATES_FOLDER, template_path)

    dir_path, file_name = os.path.split(full_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(full_path, 'w') as file:
        file.write(content)


def get_endpoints(app_name: str):
    views = get_views(app_name)
    paths = get_paths(app_name)

    endpoints: list[Endpoint] = []

    for view in views:
        endpoint = get_endpoint(view, paths, app_name)
        if endpoint.view_type:
            endpoints.append(endpoint)

    return endpoints


def get_endpoint(view, paths: list[Path], app_name: Optional[str]):
    path_name = None

    for path in paths:
        if path.view == view.__name__:
            path_name = path.path_name

    path_name = f"{app_name}:{path_name}" if app_name else path_name
    view_type = get_view_type(view.__name__)
    model = view.model

    return Endpoint(view, view.template_name, path_name, model, view_type)


def get_views(app_name: str):
    views_module = get_views_module(app_name)
    return import_views(views_module)


def get_paths(app_name: str):
    urls_py = open(os.path.join(app_name, "urls.py"), "r").read()
    return extract_paths(urls_py)


def get_view_type(view: str):
    if view.endswith(ViewType.CREATE.value):
        return ViewType.CREATE

    if view.endswith(ViewType.UPDATE.value):
        return ViewType.UPDATE

    if view.endswith(ViewType.DETAIL.value):
        return ViewType.DETAIL

    if view.endswith(ViewType.LIST.value):
        return ViewType.LIST
    else:
        return None
