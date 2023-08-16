# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensesame_plugins',
 'opensesame_plugins.audio_low_Latency',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_init',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_pause',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_resume',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_start',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_stop',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_play_wait',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_init',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_pause',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_resume',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_start',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_stop',
 'opensesame_plugins.audio_low_Latency.audio_low_latency_record_wait']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2',
 'opensesame-core>=4.0.0a0',
 'pyalsaaudio>=0.8.4',
 'pyaudio>=0.2.13',
 'pygame>=2.1.2',
 'sounddevice>=0.4.6']

setup_kwargs = {
    'name': 'opensesame-plugin-audio-low-latency',
    'version': '10.0.0',
    'description': 'An OpenSesame Plug-in for playing and recording audio files with low latency on Linux',
    'long_description': "OpenSesame Plug-in: Audio Low Latency\n==========\n\n*An OpenSesame plug-in for playing and recording audio files with low latency.*  \n\nCopyright, 2022, Bob Rosbag\n\n\n## 1. About\n--------\n\nThe main goal of this plug-in is to play and record audio with minimal and predictable latencies to achieve a high accuracy and precision. The 'PyAlsaAudio' package which uses the Linux ALSA audio system provided the best results within Python. \n'PortAudio' and 'sounddevice' are cross-platform and work on both Windows as Linux.\n\nThis plug-in consist of playback and recording items as well as foreground as background (multi-threaded) items.\nBoth playback and recording have their own *init* item. These should be placed at the beginning of an experiment.\n\n\nDifference between foreground and background:\n\n- **Foreground** items play/record until the file ends or the set duration has passed. \n- **Background** items consist of a 'start', 'wait' and 'stop' item. These are fully multi-threaded. After the start of the playback/recording, the item will immediately advance to the next item. When it reaches the 'stop' or 'wait' item, it will stop the audio or wait until the file ends or duration has passed.\n\n\nSeven items for playback:\n\n- **Play Init** initialization of the playback audio device, this should be placed at the beginning of an experiment.\n\nForeground:\n- **Play** starts the playback of audio, it will play the entire audio file or will stop after the set duration has passed before continuing to the next item in the experiment.\n\nBackground:\n- **Play Start** starts the playback of audio, it will directly advance to the next item in the experiment.\n- **Play Wait** waits until the thread from 'Play Start' is finished (end of audio or surpassing the duration) before advancing to the next item in the experiment.\n- **Play Stop** sends a stop signal to the 'Play Start' thread to stop immediately and checks if the thread has finished.\n\n- **Play Pause** pauses playback of audio.\n- **Play Resume** resumes playback of audio.\n\n\nSeven items for recording:\n\n- **Record Init** initialization of the playback audio device, this should be placed at the beginning of an experiment.\n\nForeground:\n- **Record** starts the recording of audio, it will record for the set duration before continuing to the next item in the experiment.\n\nBackground:\n- **Record Start** starts the recording of audio, it will directly advance to the next item in the experiment.\n- **Record Wait** waits until the thread from 'Record Start' is finished (surpassing the duration) before advancing to the next item in the experiment.\n- **Record Stop** sends a stop signal to the 'Record Start' thread to stop immediately and checks if the thread has finished.\n\n- **Record Pause** pauses recording of audio.\n- **Record Resume** resumes recording of audio.\n\n\nTimestamps can be found in the log file by the name: time_stimulus_onset_[item_name]\n\n\nKnown bugs:\n\n- Recording with the PyAudio module does not seem to work at the moment\n\n\n\n## 2. LICENSE\n----------\n\nThe Audio Low Latency plug-in is distributed under the terms of the GNU General Public License 3.\nThe full license should be included in the file COPYING, or can be obtained from\n\n- <http://www.gnu.org/licenses/gpl.txt>\n\nThis plug-in contains works of others. Icons are derivatives of the Faience icon theme, Faenza icon theme and Papirus icon theme.\n\n\n## 3. Documentation\n----------------\n\nInstallation instructions and documentation on OpenSesame are available on the documentation website:\n\n- <http://osdoc.cogsci.nl/>\n",
    'author': 'Bob Rosbag',
    'author_email': 'debian@bobrosbag.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dev-jam/opensesame-plugin-audio_low_latency',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
