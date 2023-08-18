# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geopkg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'geopkg',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `geopkg`\n\nLightweight utilities for geopackage management.\n',
    'author': 'ellsphillips',
    'author_email': 'elliott.phillips.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
