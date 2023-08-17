# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forcha']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=1.0.1,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'timm>=0.9,<0.10',
 'torch==2.0.0',
 'torchaudio==2.0.1',
 'torchvision==0.15.1']

setup_kwargs = {
    'name': 'forcha',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Maciej Zuziak',
    'author_email': 'maciejkrzysztof.zuziak@isti.cnr.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Scolpe/forcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
