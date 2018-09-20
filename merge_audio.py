# -*- coding:utf-8 -*-
# Author: yuyongsheng
# Time: 18-9-17 上午9:49
# Description:

import os
from pydub import AudioSegment

project_path = os.getcwd()
data_path = project_path + '/silence_audio'

for root, dirs, files in os.walk(data_path):
    sound_list = []
    for filename in files:
        wav_file = os.path.join(root + '/'+filename)
        sound = AudioSegment.from_wav(wav_file)
        sound_list.append(sound)
    sound_file = sound_list[0]
    for i in xrange(1, len(sound_list), 1):
        sound_file = sound_file.append(sound_list[i], crossfade=0)
    sound_file.export(root + '/silence_audio.wav', format= "wav")


