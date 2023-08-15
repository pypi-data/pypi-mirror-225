# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_mentions',
 'webint_mentions.templates',
 'webint_mentions.templates.received',
 'webint_mentions.templates.sent']

package_data = \
{'': ['*']}

install_requires = \
['webint>=0.0']

entry_points = \
{'webapps': ['mentions = webint_mentions:app']}

setup_kwargs = {
    'name': 'webint-mentions',
    'version': '0.0.10',
    'description': 'manage mentions on your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
