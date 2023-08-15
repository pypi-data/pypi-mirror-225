# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cstx']

package_data = \
{'': ['*']}

install_requires = \
['decord',
 'easydict',
 'einops',
 'ftfy',
 'librosa',
 'pytorch-lightning',
 'six',
 'timm',
 'torchlibrosa',
 'tqdm',
 'transformers']

setup_kwargs = {
    'name': 'cstx',
    'version': '0.1.0',
    'description': 'Description of the cstx package',
    'long_description': 'None',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
