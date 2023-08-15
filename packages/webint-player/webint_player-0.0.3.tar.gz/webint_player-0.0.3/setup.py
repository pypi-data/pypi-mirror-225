# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_player', 'webint_player.templates']

package_data = \
{'': ['*']}

install_requires = \
['webagt>=0.0', 'webint>=0.0']

entry_points = \
{'webapps': ['player = webint_player:app']}

setup_kwargs = {
    'name': 'webint-player',
    'version': '0.0.3',
    'description': 'play media on your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/webint-player',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
