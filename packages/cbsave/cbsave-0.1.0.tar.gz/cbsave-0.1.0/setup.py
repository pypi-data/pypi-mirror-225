# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbsave']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=10.0.0,<11.0.0']

setup_kwargs = {
    'name': 'cbsave',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
