# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rozetka',
 'rozetka.entities',
 'rozetka.examples',
 'rozetka.runners',
 'rozetka.tools']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-retry>=2.8.3,<3.0.0',
 'global-logger>=0.3.30,<0.4.0',
 'influxdb[async]>=5.3.1,<6.0.0',
 'knockknock>=0.1.8.1,<0.2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pip>=22.2.2,<23.0.0',
 'progress>=1.6,<2.0',
 'python-worker>=1.10.1,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'rozetka-api',
    'version': '1.1.6',
    'description': 'Rozetka Python API',
    'long_description': 'Rozetka.ua Python API\n---------------------\n\nExamples\n^^^^^^^^\n\nrozetka/examples/example_item.py\n\nrozetka/examples/example_category.py\n\nGithub\n^^^^^^^^\nhttps://github.com/ALERTua/rozetka_api\n\nPyPi\n^^^^^^^^\nhttps://pypi.org/project/rozetka-api/\n',
    'author': 'Alexey ALERT Rubasheff',
    'author_email': 'alexey.rubasheff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ALERTua/rozetka_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
