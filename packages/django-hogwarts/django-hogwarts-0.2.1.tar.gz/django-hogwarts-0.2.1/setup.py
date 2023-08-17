# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hogwarts',
 'hogwarts.magic_templates',
 'hogwarts.magic_urls',
 'hogwarts.magic_views',
 'hogwarts.management',
 'hogwarts.management.commands',
 'hogwarts.migrations',
 'hogwarts.tests',
 'hogwarts.tests.template_tests',
 'hogwarts.tests.url_tests',
 'hogwarts.tests.view_tests']

package_data = \
{'': ['*'], 'hogwarts': ['scaffold/*']}

install_requires = \
['Django==4.2.3',
 'Jinja2>=3.1.2,<4.0.0',
 'coverage>=7.2.7,<8.0.0',
 'crispy-bootstrap5==0.6',
 'django-crispy-forms>=2.0,<3.0',
 'rich>=13.5.2,<14.0.0',
 'ruff>=0.0.280,<0.0.281']

setup_kwargs = {
    'name': 'django-hogwarts',
    'version': '0.2.1',
    'description': 'Django utilities for codegen and DX improvement',
    'long_description': '<h1 align="center">Django hogwarts 🧙\u200d♂️</h1>\n<h4 align="center">Management commands to generate views, urls and templates!</h4>\n\n> [!WARNING]\n> Customization and documentation are incomplete \n\nUse CLI commands to generate:\n- basic create, update, list, detail views\n- urlpatterns from views with REST like path urls\n- form, table, detail templates (Bootstrap and django-crispy-forms by default)\n\n[checkout docs](https://django-hogwarts.vercel.app/)\n\n---\n\n## Installation\n```shell\n# pip\npip install django-hogwarts\n\n# poetry\npoetry add --dev django-hogwarts\n```\n\nadd `hogwarts` to your `INSTALLED_APPS`:\n``` python\nINSTALLED_APPS = [\n    ...\n    "hogwarts"\n]\n```\n\n## Usage\n\n### Generate urls.py\n\n```\npython manage.py genurls <your-app-name>\n```\n\nArguments:\n- `--merge`, `-m` add new paths without changing existing paths in urls.py\n- `--force-app-name`, `fan` override app_name in urls.py \n\n### Generate views.py\n```\npython manage.py genviews <your-app-name> <model-name>\n```\nArguments\n- `smart-mode`, `-s` adds login required, sets user for CreateView and checks if client is owner of object in UpdateView\n- `model-is-namespace`, `-mn` adds success_url with name model as [namespace](https://docs.djangoproject.com/en/4.2/topics/http/urls/#url-namespaces)\n\n### Generate templates\n``` \npython manage.py gentemplates <your-app-name>\n```\n',
    'author': 'adiletto64',
    'author_email': 'adiletdj19@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adiletto64/django-hogwarts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
