# encoding: utf-8
"""
Roby ---- an open source AI talking chatbot
Copyright (C) 2014 Mark Young <ideamark@qq.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys,os,re
import time
import aiml
import wave
import pyaudio
import pocketsphinx
import sphinxbase
import serial

# English speaking function
def speak_en(outputString):
    print 'Roby: ' + outputString
    # use festival for English tts speaking
    os.system('echo "' + outputString + '"|festival --tts')

# Chinese speaking function
def speak_cn(outputString):
    print 'Roby: ' + outputString
    # use ekho for Chinese tts speaking
    os.system('ekho -s 150 -r -25 -a -30 "' + outputString + '"')

# CMU Sphinx decoding function
def decodeSpeech(wavfile,hmm,lm,dic):
    # Create a decoder with certain model
    config = pocketsphinx.Decoder.default_config()
    config.set_string('-hmm', hmm)
    config.set_string('-lm', lm)
    config.set_string('-dict', dic)
    speechRec = pocketsphinx.Decoder(config)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    # This used to fix a bug
    if speechRec.hyp() == None:
        return ''
    else:
        return speechRec.hyp().hypstr

# function for regex checking
def sameStr(string,regex):
    pattern = re.compile(regex)
    return pattern.match(string)

if __name__ == '__main__':
    
    # this value is for my device. You must change it before running Roby
    ttyPath = '/dev/ttyUSB3'

    # Initial value for pyserial
    s = serial.Serial(ttyPath,115200,timeout=1)
    if s.isOpen():
        print s.portstr + ' opened'
    else:
        print 'Can not open Serial Port'
        os._exit(0)

    # Initial value for pyaiml
    k = aiml.Kernel()
    k.learn("./aiml/*")
    k.respond("load aiml b")
    
    # initial value for pyaudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3
     
    # start the loop
    speak_en('Roby is ready to work, sir')
    action = False
    mode = 'english'
    while True: 
        fn = 'record.wav'
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print 'recording ...'
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print 'done recording'
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(fn, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        wavfile = fn
        if wavfile == None:
            continue
        # the CMU Sphinx module, which you can change
        if mode == 'english':
            hmm = '/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k'
            if not action:
                lm = './model/en/name_en.lm'
                dic = './model/en/name_en.dic'
            else:
                lm = './model/en/command_en.lm'
                dic = './model/en/command_en.dic'
        elif mode == 'chinese':
            hmm = '/usr/local/share/pocketsphinx/model/hmm/zh/tdt_sc_8k'
            if not action:
                lm = './model/zh/name_cn.lm'
                dic = './model/zh/name_cn.dic'
            else:
                lm = './model/zh/command_cn.lm'
                dic = './model/zh/command_cn.dic'
        recognised = decodeSpeech(wavfile,hmm,lm,dic)
        inputString = recognised
        print 'action = ' + str(action)
        print 'You: ' + inputString
        if inputString == '':
            continue
        if mode == 'english':
            if sameStr(inputString,'^ROBY.*'):
                speak_en('yes, sir')
                action = True
                continue
        elif mode == 'chinese':
            if sameStr(inputString,'^罗比.*'):
                speak_cn('是的，先生')
                action = True
                continue
        if action:
            action = False
            if mode == 'english':
                if sameStr(inputString,'^EXIT.*'):
                    respond = k.respond(inputString)
                    speak_en('Good bye, sir')
                    os._exit(0)
                elif 'CHINESE MODE' in inputString:
                    mode = 'chinese'
                    speak_cn('已进入中文模式，先生')
                elif 'WRITE SERIAL PORT' in inputString:
                    speak_en('write serial port, sir')
                    s.write('hello, I am Roby\n')
                else:
                    respond = k.respond(inputString)
                    speak_en(respond)
                    if sameStr(respond,'.*\?$'):
                        action = True
            elif mode == 'chinese':
                if '英文模式' in inputString:
                    mode = 'english'
                    speak_en('returned to English mode')
                elif '几点' in inputString:
                    speak_cn(time.strftime("%Y年%m月%d日，%H时%M分%S秒", time.localtime()))
