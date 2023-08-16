# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiktokx']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0', 'scipy>=1.7,<2.0', 'torch>=1.10,<2.0']

setup_kwargs = {
    'name': 'tiktokx',
    'version': '0.1.0',
    'description': 'The rhythm of algorithms, dancing through recommendation streams.',
    'long_description': 'None',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
