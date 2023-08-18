# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lca_third_party']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lca-third-party',
    'version': '0.1.1',
    'description': 'Exemplary third party library for LCA 2023',
    'long_description': 'None',
    'author': 'Michał Chałupczak',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
