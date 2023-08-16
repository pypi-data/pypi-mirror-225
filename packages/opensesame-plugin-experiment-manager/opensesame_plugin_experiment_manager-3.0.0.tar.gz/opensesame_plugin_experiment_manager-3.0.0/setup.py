# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.experiment_manager',
 'opensesame_plugins.experiment_manager.experiment_manager']

package_data = \
{'': ['*']}

install_requires = \
['opensesame-core>=4.0.0a0']

setup_kwargs = {
    'name': 'opensesame-plugin-experiment-manager',
    'version': '3.0.0',
    'description': 'An OpenSesame Plug-in for managing/executing multiple OpenSesame experiments.',
    'long_description': 'OpenSesame Plug-in: Experiment Manager\n==========\n\n*An OpenSesame plug-in for managing/executing multiple OpenSesame experiments.*  \n\nCopyright, 2022, Bob Rosbag  \n\n\n## 1. About\n--------\n\nThis plug-in can insert standalone OpenSesame Experiments within a main experiment. \nIt can run within a loop or sequence as an item. This makes it possible to run a number \nof experiments in sequence (random or fixed order) and also it gives the possibility to \ngive each experiment its own (different) backend. \n\nThis plug-in has three options:\n\n- *Dummy mode* for testing experiments.\n- *Verbose mode* for testing experiments.\n- *Experiment file name* for Windows: hexadecimal or decimal value, for Linux: full path or port number.\n\n\n## 2. LICENSE\n----------\n\nThe Experiment Manager plug-in is distributed under the terms of the GNU General Public License 3.\nThe full license should be included in the file COPYING, or can be obtained from\n\n- <http://www.gnu.org/licenses/gpl.txt>\n\nThis plug-in contains works of others.\n  \n  \n## 3. Documentation\n----------------\n\nInstallation instructions and documentation on OpenSesame are available on the documentation website:\n\n- <http://osdoc.cogsci.nl/>\n',
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-experiment_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
