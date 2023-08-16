# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiktokx']

package_data = \
{'': ['*']}

install_requires = \
['dgl', 'numpy', 'scipy', 'torch', 'visdom']

setup_kwargs = {
    'name': 'tiktokx',
    'version': '0.1.3',
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
}


setup(**setup_kwargs)
