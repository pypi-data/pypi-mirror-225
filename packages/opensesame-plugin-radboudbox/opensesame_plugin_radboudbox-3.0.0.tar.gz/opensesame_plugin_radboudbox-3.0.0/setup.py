# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.radboudbox',
 'opensesame_plugins.radboudbox.radboudbox_get_buttons_start',
 'opensesame_plugins.radboudbox.radboudbox_get_buttons_wait',
 'opensesame_plugins.radboudbox.radboudbox_init',
 'opensesame_plugins.radboudbox.radboudbox_send_control',
 'opensesame_plugins.radboudbox.radboudbox_send_trigger',
 'opensesame_plugins.radboudbox.radboudbox_wait_buttons']

package_data = \
{'': ['*']}

install_requires = \
['opensesame-core>=4.0.0a0', 'rusocsci>=0.9.2']

setup_kwargs = {
    'name': 'opensesame-plugin-radboudbox',
    'version': '3.0.0',
    'description': 'An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems',
    'long_description': "OpenSesame Plug-in: Radboud Buttonbox\n==========\n\n*An OpenSesame plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  \n\nCopyright, 2022, Bob Rosbag\n\nThis plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. \n  \n  \n## 1. About\n--------\n\nThe Technical Support Group (Radboud University, Social Sciences) developed an USB Arduino based Buttonbox which can be used for time accurate(1ms) button press, voice key, sound key registration and sending parallel port like triggers.\nUpper case A, B, C, D, E, F are used for key presses, and lower case a, b, c, d, e, f are used for key releases. Uppercase S is used for sound key detection and uppercase V for voice key.  \n\nFor more information:\n\n<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>\n\n\nThis plug-in consist of foreground and background (multithreaded) items.\n\n\nDifference between foreground and background:\n\n- **Foreground** item starts button/signal registration until it detects an allowed button or the set duration has passed. \n- **Background** item consist of a 'start' and 'wait' item. These are fully multi-threaded. After the start of the button/signal registration, the item will immediately advance to the next item. When the experiment reaches the 'wait' item, it will wait until a button/signal has been detected by the 'start' item or the duration has passed.\n\n\nThis plug-in has six items:\n\n- **Init** initialization of the buttonbox, this should be placed at the beginning of an experiment.\n- **Wait Buttons** waits for a button press or release before continuing to the next item in the experiment\n- **Get Buttons Start** starts a new thread which monitors for button presses/releases, it will directly advance to the next item in the experiment\n- **Get buttons Wait** waits until the thread from 'Get Buttons Start' is finished (has detected a button press/release) before advancing to the next item in the experiment \n- **Send Control** send control code to the buttonbox, for example 'Calibrate Sound', 'Detect Sound'\n- **Send Trigger** for sending triggers to hardware with a parallel port\n\n\nTimestamps can be found in the logs by the name: time_response_[item_name]\n\n\nLinux, and Windows are supported (possible also OSX, not tested). The plug-in will first look for the globally installed rusocsci package. If this is not available, the shipped version will be used. Install options are listed below.\n  \n  \n## 2. LICENSE\n----------\n\nThe Radboud Buttonbox plug-in is distributed under the terms of the GNU General Public License 3.\nThe full license should be included in the file COPYING, or can be obtained from\n\n- <http://www.gnu.org/licenses/gpl.txt>\n\nThis plug-in contains works of others.\n  \n  \n## 3. Documentation\n----------------\n\nInstallation instructions and documentation on OpenSesame are available on the documentation website:\n\n- <http://osdoc.cogsci.nl/>\n",
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-radboudbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
