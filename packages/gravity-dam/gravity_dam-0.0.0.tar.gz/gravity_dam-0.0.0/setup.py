# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gravity_dam']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gravity-dam',
    'version': '0.0.0',
    'description': "A Python library that combines various stream constraints and stream regularization algorithms. (It's like a gravity dam that uses itself to resist the pressure of the water)",
    'long_description': '# gravity-dam\nGravity dam resists water pressure and other external forces through its own gravity\n',
    'author': 'so1n',
    'author_email': 'so1n897046026@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
