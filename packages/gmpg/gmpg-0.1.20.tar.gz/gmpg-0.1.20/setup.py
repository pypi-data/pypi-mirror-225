# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gmpg', 'gmpg._pkg', 'gmpg._pkg.licensing']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.7.0,<24.0.0',
 'ipython>=8.14.0,<9.0.0',
 'isort>=5.11.4,<6.0.0',
 'mock>=5.0.1,<6.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pip>=23.2.1,<24.0.0',
 'pydeps>=1.11.0,<2.0.0',
 'pyright>=1.1.322,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest-gevent>=1.1.0,<2.0.0',
 'pytest-pep8>=1.0.6,<2.0.0',
 'pytest>=7.4.0,<8.0.0',
 'radon>=5.1.0,<6.0.0',
 'responses>=0.22.0,<0.23.0',
 'toml>=0.10.2,<0.11.0',
 'txtint>=0.1']

entry_points = \
{'console_scripts': ['gmpg = gmpg.__main__:main']}

setup_kwargs = {
    'name': 'gmpg',
    'version': '0.1.20',
    'description': 'tools for metamodern software development',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/gmpg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
