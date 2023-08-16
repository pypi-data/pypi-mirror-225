# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.parallel_port_trigger',
 'opensesame_plugins.parallel_port_trigger.parallel_port_trigger_init',
 'opensesame_plugins.parallel_port_trigger.parallel_port_trigger_send']

package_data = \
{'': ['*']}

install_requires = \
['opensesame-core>=4.0.0a0', 'pyparallel>=0.2.2']

setup_kwargs = {
    'name': 'opensesame-plugin-parallel-port-trigger',
    'version': '4.0.0',
    'description': 'An OpenSesame Plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems',
    'long_description': 'OpenSesame Plug-in: Parallel Port Trigger\n==========\n\n*An OpenSesame plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  \n\nCopyright, 2022, Bob Rosbag  \n\nContributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.\n\n\n## 1. About\n--------\n\nIn EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.\n\nThe plug-in has an *init* item which should be placed at the beginning of an experiment and a *trigger* item for initiating triggers:\n\n- *Dummy mode* for testing experiments.\n- *Port adress* for Windows: hexadecimal or decimal value, for Linux: full path or port number.\n- *Value* is a positive integer between 1-255 and specifies the trigger byte.\n- *Enable duration* option to enable the duration parameter.\n- *Duration* is the duration in ms.\n\n\nLinux and Windows are supported (possible also OSX, not tested). For Windows the `DLPortIO.dll` driver is used to access the parallel port. No need for driver installation.\n\n\nDocumentation: <http://osdoc.cogsci.nl/devices/triggers/>\n\n\n## 2. LICENSE\n----------\n\nThe Parallel Port Trigger plug-in is distributed under the terms of the GNU General Public License 3.\nThe full license should be included in the file COPYING, or can be obtained from\n\n- <http://www.gnu.org/licenses/gpl.txt>\n\nThis plug-in contains works of others.\n\n\n## 3. Documentation\n----------------\n\nInstallation instructions and documentation on OpenSesame are available on the documentation website:\n\n- <http://osdoc.cogsci.nl/>\n',
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
