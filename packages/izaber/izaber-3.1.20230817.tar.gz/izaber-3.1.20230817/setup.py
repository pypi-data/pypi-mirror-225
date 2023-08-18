# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izaber']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3',
 'PyYAML>=5.3.0,!=5.4.1,!=6.0',
 'appdirs>=1.4.4',
 'docopt>=0.6.2',
 'python-dateutil>=2.8.1',
 'pytz>=2021.1',
 'six>=1.15.0']

extras_require = \
{'email': ['beautifulsoup4>=4.9.3', 'lxml>=4.6.2']}

setup_kwargs = {
    'name': 'izaber',
    'version': '3.1.20230817',
    'description': 'Base load point for iZaber code',
    'long_description': 'None',
    'author': 'Aki Mimoto',
    'author_email': 'aki@zaber.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0,<4.0',
}


setup(**setup_kwargs)
