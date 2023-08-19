# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vars_gridview',
 'vars_gridview.lib',
 'vars_gridview.lib.m3',
 'vars_gridview.scripts',
 'vars_gridview.ui',
 'vars_gridview.ui.settings',
 'vars_gridview.ui.settings.tabs']

package_data = \
{'': ['*'],
 'vars_gridview': ['assets/base_query.sql',
                   'assets/base_query.sql',
                   'assets/gridview.ui',
                   'assets/gridview.ui',
                   'assets/style/*']}

install_requires = \
['beholder-client>=0.1.0,<0.2.0',
 'opencv-python-headless>=4.5.5.62,<5.0.0.0',
 'pymssql>=2.2.4,<3.0.0',
 'pyqt6>=6.4.0,<7.0.0',
 'pyqtgraph>=0.13.0,<0.14.0',
 'qdarkstyle>=3.0.3,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'sharktopoda-client==0.4.0']

entry_points = \
{'console_scripts': ['vars-gridview = vars_gridview.scripts.run:main']}

setup_kwargs = {
    'name': 'vars-gridview',
    'version': '0.3.3',
    'description': 'VARS GridView is a tool for reviewing and correcting VARS localizations in bulk.',
    'long_description': '# vars-gridview\n\n**VARS GridView** is a tool for reviewing and correcting VARS localizations in bulk.\n\n[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/)\n\nAuthors: Kevin Barnard ([kbarnard@mbari.org](mailto:kbarnard@mbari.org)), Paul Roberts ([proberts@mbari.org](mailto:proberts@mbari.org))\n\n---\n\n## Install\n\n### From PyPI\n\nVARS GridView is available on PyPI as `vars-gridview`. To install, run:\n\n```bash\npip install vars-gridview\n```\n\n### From source\n\nThis project is built with [Poetry](https://python-poetry.org/). To install from source, run (in the project root):\n\n```bash\npoetry install\n```\n\n## Run\n\nOnce VARS GridView is installed, you can run it from the command line:\n\n```bash\nvars-gridview\n```\n\nYou will first be prompted to log in. Enter your VARS username and password. \n\n*Note: If you are not using MBARI production VARS, change the "Config server" field to point to your instance of Raziel. This setting is persisted.*\n\n---\n\nCopyright &copy; 2020&ndash;2023 [Monterey Bay Aquarium Research Institute](https://www.mbari.org)',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mbari-org/vars-gridview',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
