# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gojira',
 'gojira.auth',
 'gojira.filters',
 'gojira.generics',
 'gojira.permissions']

package_data = \
{'': ['*']}

install_requires = \
['classy-fastapi>=0.2.12,<0.3.0',
 'fastapi>=0.85.1,<0.86.0',
 'ormar>=0.12.0,<0.13.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'gojira',
    'version': '0.1.2',
    'description': 'Lightweight framework to build a RESTful applications',
    'long_description': 'None',
    'author': 'Dimash',
    'author_email': 'd.igisinov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
