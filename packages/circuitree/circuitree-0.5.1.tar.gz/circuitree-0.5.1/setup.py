# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circuitree']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.1,<4.0', 'numpy>=1.23.0,<2.0.0']

extras_require = \
{'examples': ['numba>=0.57.0',
              'psutil>=5.9.4,<6.0.0',
              'ray[default]>=2.4.0,<3.0.0',
              'pandas>=2.0.0,<3.0.0',
              'tables>=3.8.0,<4.0.0',
              'pyarrow>=12.0.0,<13.0.0',
              'h5py>=3.8.0,<4.0.0',
              'more-itertools>=9.1.0,<10.0.0',
              'matplotlib>=3.7.1,<4.0.0',
              'seaborn>=0.12.2,<0.13.0',
              'tqdm>=4.65.0,<5.0.0'],
 'examples:python_version >= "3.10" and python_version < "3.12"': ['scipy>=1.10.1,<2.0.0'],
 'parallel': ['psutil>=5.9.4,<6.0.0',
              'ray[default]>=2.4.0,<3.0.0',
              'pandas>=2.0.0,<3.0.0',
              'tables>=3.8.0,<4.0.0',
              'pyarrow>=12.0.0,<13.0.0',
              'h5py>=3.8.0,<4.0.0']}

setup_kwargs = {
    'name': 'circuitree',
    'version': '0.5.1',
    'description': 'Genetic circuit design using Monte Carlo tree search',
    'long_description': '# CircuiTree\nGenetic circuit design using Monte Carlo tree search\n\n## Installation\n\n### From a package repository\nTo install using `pip`:\n\n```pip install circuitree```\n\n### From the GitHub repository\n\nTo install and use `circuitree` from the GitHub source code, first clone the repo into a directory.\n\n```git clone https://github.com/pranav-bhamidipati/circuitree.git[ dir_name]```\n\nThen, you can build the environment using the command-line tool `poetry`. Instructions for installation can be [found here](https://python-poetry.org/). \n\nFrom the main project directory, run `poetry install` to install a virtual environment with `circuitree` installed. The easiest way to use this environment is to run it interactively with `poetry shell`. Alternatively, you can run a command in the virtual environment with `poetry run <command>`. For instance, to launch a Jupyter notebook with `circuitree` pre-loaded, run `poetry run jupyter notebook`. \n\n## Usage\n\nSee the [quick-start demo](examples/quick_start.ipynb).\n',
    'author': 'pranav-bhamidipati',
    'author_email': 'pbhamidi@usc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
