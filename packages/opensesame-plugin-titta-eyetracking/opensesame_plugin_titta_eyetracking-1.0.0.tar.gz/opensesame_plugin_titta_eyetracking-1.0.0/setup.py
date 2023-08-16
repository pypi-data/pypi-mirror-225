# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.titta',
 'opensesame_plugins.titta.titta_calibrate',
 'opensesame_plugins.titta.titta_init',
 'opensesame_plugins.titta.titta_send_message',
 'opensesame_plugins.titta.titta_start_recording',
 'opensesame_plugins.titta.titta_stop_recording']

package_data = \
{'': ['*']}

install_requires = \
['opensesame-core>=4.0.0a0', 'titta>=1.9.0', 'tittapy>=1.0.0']

setup_kwargs = {
    'name': 'opensesame-plugin-titta-eyetracking',
    'version': '1.0.0',
    'description': 'Titta Eye Tracking plugin for OpenSesame',
    'long_description': "# OpenSesame Plugin: Titta Eye Tracking\n\n*Copyright, 2023, Bob Rosbag, Diederick C. Niehorster & Marcus Nyström*\n\n## About\n\nThis plugin implements Titta in OpenSesame for Eye Tracking. \n\nTitta is a toolbox for using eye trackers from Tobii Pro AB with Python, specifically offering integration with PsychoPy. A Matlab version that integrates with PsychToolbox is also available from https://github.com/dcnieho/Titta. For a similar toolbox for SMI eye trackers, please see www.github.com/marcus-nystrom/SMITE.\n\nCite as: Niehorster, D.C., Andersson, R. & Nystrom, M. (2020). Titta: A toolbox for creating PsychToolbox and Psychopy experiments with Tobii eye trackers. Behavior Research Methods. doi: 10.3758/s13428-020-01358-8\n\nPlease mention: Bob Rosbag as creator of this plugin\n\nFor questions, bug reports or to check for updates, please visit https://github.com/marcus-nystrom/Titta.\n\nTo minimize the risk of missing samples, the current repository uses TittaPy (pip install TittaPy), a C++ wrapper around the Tobii SDK, to pull samples made available from the eye tracker.\n\n\n## License\n\nThe Titta Eye Tracking plugin is distributed under the terms of the Creative Commons Attribution 4.0 International Public License\nThe full license should be included in the file LICENSE.md\n\n\n## Known bugs\n\n- In dummy mode, when the experiment is finished, OpenSesame will not return to the GUI. The button with the cross and text: 'Forcibly kill the experiment' has to be used to end the session and get back to the GUI. This only happens when in dummy mode and the cause resides somewhere in the 'calibrate' command.\n",
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-titta_eyetracking',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
