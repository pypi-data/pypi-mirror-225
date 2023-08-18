# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_handy_admin']

package_data = \
{'': ['*'], 'django_handy_admin': ['templates/admin/*']}

install_requires = \
['django==4.2']

setup_kwargs = {
    'name': 'django-handy-admin',
    'version': '0.0.0',
    'description': 'Set of handy addons to Django Admin.',
    'long_description': '# Django Handy Admin\n\nThis is an empty project yet.\n',
    'author': 'Michał Sut',
    'author_email': 'sut.michal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
