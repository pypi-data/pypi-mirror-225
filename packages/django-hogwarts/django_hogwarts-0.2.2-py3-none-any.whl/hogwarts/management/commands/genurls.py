import os

from django.core.management.base import BaseCommand
from rich.console import Console
from rich.syntax import Syntax

from hogwarts.magic_urls.gen_urls import UrlGenerator, urlpatterns_is_empty, UrlMerger
from .base import get_app_config, get_views_module


console = Console()


class Command(BaseCommand):
    help = "urlpatterns generation from views.py"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument(
            "--merge", "-m",
            action="store_true",
            help="add urls to existing urlpatterns without overriding whole file"
        )

        parser.add_argument(
            "--force-app-name", "-fan",
            action="store_true",
            help="use given app name rather than app_name in urls.py"
        )

    def handle(self, *args, **options):
        app_name: str = options["app_name"]
        merge: bool = options["merge"]
        force_new_app_name: bool = options["force_app_name"]

        views_module = get_views_module(app_name)
        app_config = get_app_config(app_name)
        urls_path = os.path.join(app_config.path, "urls.py")

        url_generator = UrlGenerator(views_module, urls_path, app_name, force_new_app_name)
        url_merger = UrlMerger(views_module, urls_path, app_name, force_new_app_name)

        if merge:
            url_merger.merge_urls_py()
            console.print("new paths merged to urlpatterns ✅", style="green")
        else:
            code = open(urls_path, "r").read()
            if not urlpatterns_is_empty(code):
                # alert user that urls is not empty
                console.print(
                    "\nLooks like you have some paths in urlpatterns. 🚧\n"
                    f"{urls_path}:",
                    style="bold yellow"
                )
                print("===================")
                Console().print(Syntax(code, "python"))
                print("===================")

                # get user input until correct
                while True:
                    print("Do you want fully override urls or merge?")
                    response = input("write (o)-override, (m)-merge or (c) to cancel: ")
                    if response not in ["m", "o", "c"]:
                        print("wrong command!")
                        continue

                    if response == "m":
                        url_merger.merge_urls_py()
                        console.print("new paths merged to urlpatterns ✅", style="green")

                    elif response == "o":
                        url_generator.gen_urls_py()
                        console.print("urlpatterns have been generated ✅", style="green")

                    elif response == "c":
                        print("canceled")
                    return
            else:
                url_generator.gen_urls_py()
                console.print("urlpatterns have been generated ✅", style="green")

