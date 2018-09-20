# -*- coding:utf-8 -*-
# Author: yuyongsheng
# Time: 18-9-17 下午5:05
# Description:

import os
import numpy as np
from pydub import AudioSegment

project_path = os.getcwd()
file_path = project_path + '/silence_audio.wav'

sound = AudioSegment.from_wav(file_path)
sound_array = sound.get_array_of_samples()
frame_rate = sound.frame_rate
window_length = int(0.1 * frame_rate)

energy = []
for i in xrange(int(len(sound_array) / window_length)):
    # energy
    win_data = sound_array[window_length * i: window_length * (i + 1)]
    win_data_flo = np.array(win_data, dtype=np.float)
    en = (np.dot(win_data_flo, win_data_flo.T))
    if en < 0:
        print win_data_flo
        exit()
    energy.append(en)
sum = 0
for i in energy:
    sum = sum + i
print(np.sqrt(sum/len(energy)))
