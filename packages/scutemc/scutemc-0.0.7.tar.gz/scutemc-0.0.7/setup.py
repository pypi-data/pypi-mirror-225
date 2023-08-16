# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scute', 'scute.internal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scutemc',
    'version': '0.0.7',
    'description': 'A Python library for making Minecraft datapacks.',
    'long_description': '![Title](/assets/title.png)\n\n[![Discord](https://img.shields.io/discord/1139873703556034620?label=discord)](https://discord.gg/RnRTjq24vX)\n[![GitHub Repo stars](https://img.shields.io/github/stars/t0rnato/scute?label=stars)](https://github.com/T0RNATO/scute)\n[![PyPI](https://img.shields.io/pypi/v/scute)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/scute)](https://pypi.org/project/scutemc/)\n\nA simple Python library for creating Minecraft datapacks with Python. (Very much in development)\n\n[Read the docs](https://t0rnato.github.io/scute),\n[view on PyPi](https://pypi.org/project/scutemc/), or\n[join the Discord](https://discord.gg/RnRTjq24vX) for support.',
    'author': 'TorNato',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/T0RNATO/scute',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
