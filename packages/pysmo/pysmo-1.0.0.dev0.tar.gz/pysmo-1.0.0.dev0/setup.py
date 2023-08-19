# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysmo',
 'pysmo.classes',
 'pysmo.functions',
 'pysmo.io',
 'pysmo.io.sacio',
 'pysmo.lib',
 'pysmo.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.25.2,<2.0.0',
 'pyproj>=3.5.0,<4.0.0',
 'requests>=2.31.0,<3.0.0',
 'scipy>=1.11.1,<2.0.0']

setup_kwargs = {
    'name': 'pysmo',
    'version': '1.0.0.dev0',
    'description': 'Python module for seismologists.',
    'long_description': '\n[![Test Status](https://github.com/pysmo/pysmo/actions/workflows/run-tests.yml/badge.svg)](https://github.com/pysmo/pysmo/actions/workflows/run-tests.yml)\n[![Build Status](https://github.com/pysmo/pysmo/actions/workflows/build.yml/badge.svg)](https://github.com/pysmo/pysmo/actions/workflows/build.yml)\n[![Documentation Status](https://readthedocs.org/projects/pysmo/badge/?version=latest)](https://pysmo.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/pysmo/pysmo/branch/master/graph/badge.svg?token=ZsHTBN4rxF)](https://codecov.io/gh/pysmo/pysmo)\n[![PyPI](https://img.shields.io/pypi/v/pysmo)](https://pypi.org/project/pysmo/)\n\nPysmo offers simple data types for seismologists to write code with. Instead\nof working with one big class containing all kinds of data, psymo uses separate,\nnarrowly defined classes that are more meaningful when describing things that\nexist in the real world. The type definitions are not tied to any particular\nfile format, and thus free users from needing to adhere to Python data structures\noften dictated by a rigid underlying file format.\n\nTogether with these data types, pysmo provides a growing library of essential\nfunctions that benefit from using these types. Programming with pysmo results\nin code that is:\n\n  - using modern Python concepts.\n  - easy to write and understand.\n  - both portable and future proof.\n\nPysmo itself is designed to be modular and easy to expand without interfering\nwith the existing code base, making it straightforward to incorporate user\ncontributions.\n\n## Contributors\n\n- Helio Tejedor\n',
    'author': 'Simon M. Lloyd',
    'author_email': 'simon@slloyd.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
