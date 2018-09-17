# -*- encoding:utf-8 -*-
import os
import math
import wave
import glob
import time
from pydub.audio_segment import AudioSegment
import numpy as np

# get left_endpoint
def get_left_point(index, energy):
    i = index
    try:
        while i < len(energy):
            if energy[i] > 0:
                return i;
            i = i + 1
    except:
        return None;

# get right_endpoint
def get_right_point(index, window_time, energy):
    i = index
    try:
        while i < len(energy):
            if energy[i] == 0 and (i - index) * window_time > 0.2:
                nextleft_point = get_left_point(i, energy)
                if (nextleft_point-i) * window_time > 0.5:
                    return i
            i = i + 1
    except:
        return None;



# detect speech point
def speech_separate_notRealTime(wave_raw_data): #参数为AudioSegment对象
    # 将AudioSegment对象转换为采样数组，提取音频数据
    wave_data = wave_raw_data.get_array_of_samples()
    print(len(wave_raw_data))
    print(len(wave_data))
    splited_list=[];
    framerate, nframes = wave_raw_data.frame_rate, wave_raw_data.frame_count()
    # change wave data to array data
    time = np.arange(0, nframes) * (1.0 / framerate)
    # normalized and filter noise
    data = []
    maxvalue = max(wave_data)
    for i in xrange(len(wave_data)):
        tt = (wave_data[i] * 1.0) / maxvalue
        if abs(tt) > 0.1:
            data.append(tt)
        else:
            data.append(0)
    # break point detection based on energy
    window_length = framerate / 50 #m
    # window_shift = 1
    window_time = window_length * (1.0 / framerate)
    energy = []
    # python2.7 division, float to int--round down
    for i in xrange(int(len(time) / window_length)):
        # energy
        win_data = data[window_length * i: window_length * (i + 1)]
        win_data_flo = np.array(win_data, dtype=np.float)
        en = np.dot(win_data_flo, win_data_flo.T)
        if en < 0:
            print win_data_flo
            exit()
        energy.append(en)

    i = 0;
    # len(energy) is equal to len(data)/window_length
    while i < len(energy):
        left_window_point = get_left_point(i, energy);
        if left_window_point == None:
            return splited_list
        else:
            # 检测时间较长的静音段，用于换行。
            if ((left_window_point - i) * window_time) >= 3:
                splited_list.append("return")

            right_window_point = get_right_point(left_window_point, window_time, energy);
            if right_window_point == None:
                splited_audio = wave_data[(left_window_point-1) * window_length:]
                splited_list.append(splited_audio)
            else:
                splited_audio = wave_data[(left_window_point-1) * window_length:right_window_point * window_length]
                splited_list.append(splited_audio)
        i = right_window_point
    return splited_list
