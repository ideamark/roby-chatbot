Roby-0.0
---------

Roby is an open source AI chatbot, with Local speech recognition and speech synthesis system. released under GPLv3, more details see LICENSE.

Roby-0.0 is just a demo program fragment for testing some basic functions. It only works on Linux. Supports both English and Chinese. You can watch the demo at: http://v.youku.com/v_show/id_XODExMTU1ODQ4.html

How to use:

Before runnig Roby, make sure you have installed:
* python-2.7
* pyaiml-0.8.6---------------a python AIML interpreter
* pyaudio-0.2.8--------------python bindings for portaudio
* pyserial-2.7---------------this python module encapsulates the access for the serial port
* sphinxbase-5prealpha-------the basic libraries for CMU Sphinx speech recognition engine
* pocketsphinx-5prealpha-----the CMU Sphinx speech recognition engine
* festival-2.1---------------for English TTS output
* ekho-6.0-------------------for Chinese TTS output

Python modules can be used pip or easy_install to install. Ubuntu users can use "apt-get" to install festival and ekho. sphinxbase and pocketsphinx can be compiled from source code.
You may need the web pages below:
http://www.speech.cs.cmu.edu/sphinx/doc/Sphinx.html
https://github.com/andelf/PyAIML
http://people.csail.mit.edu/hubert/pyaudio/
http://people.csail.mit.edu/hubert/pyaudio/
http://www.cstr.ed.ac.uk/projects/festival/
http://www.eguidedog.net/ekho.php

- Before running Roby, you must change the value "ttyPath" in start.py main function.
- The first line in start.py "# encoding: uft-8" can not be deleted, or it will get problems with Chinese functions.
- Roby must work with "sudo", or tty port can not be used.
- Use "sudo python start.py" to start Roby.
- You should firstly say: "Roby", then Roby says: "yes, sir", then you can say the command words.
- If Roby's respond end with "?", he will continue listen your command words without saying "Roby".
- The 0.0 version only supports several commands below:
  - how are you?
  - fine
  - what's the time?
  - what's your name?
  - how old are you?
  - chinese mode
  - write serial port
  - exit
  - 几点了？
  - 英文模式

You can build your own test speech recognition models under the folder names "model".

Any questions, email to ideamark@qq.com
