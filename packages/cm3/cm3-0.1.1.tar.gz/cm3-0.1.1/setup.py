# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cm3', 'cm3.core', 'cm3.utils']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'bitsandbytes',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'memory-profiler',
 'numpy',
 'torch',
 'transformers',
 'triton']

setup_kwargs = {
    'name': 'cm3',
    'version': '0.1.1',
    'description': 'Description of the cm3 package',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'youremail@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
