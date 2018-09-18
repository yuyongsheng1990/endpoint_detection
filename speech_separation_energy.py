# -*- coding:utf-8 -*-
# Author: yuyongsheng
# Time: 18-9-17 下午5:57
# Description:

import os
import math
import wave
import glob
import time
from pydub.audio_segment import AudioSegment
import numpy as np

E0 = 1.2 * 430542587  # 每帧的低能量阈值门限
# E1 = 2.1 * 430542587  # 每帧高能量阈值门限

# audio detection
def audio_detection(en):
    global E0
    if en > E0:
        return True
    else:
        return False

# # get left_endpoint
# def get_left_point(index, energy):
#     i = index
#     global E1
#     try:
#         while i < len(energy):
#             if energy[i] > E1:
#                 return i;
#             i = i + 1
#     except:
#         return None;
#
# # get right_endpoint
# def get_right_point(index, energy):
#     i = index
#     global E0
#     try:
#         while i < len(energy):
#             if energy[i] < E0 and i-index > 20: # 10为1s，表示语音段长度阈值为1s
#                 return i
#             i = i + 1
#     except:
#         return None;



# detect speech point
def speech_separate_notRealTime(wave_raw_data): #参数为AudioSegment对象
    # 将AudioSegment对象转换为采样数组，提取音频数据
    wave_data = wave_raw_data.get_array_of_samples()

    splited_list=[];
    framerate, nframes = wave_raw_data.frame_rate, wave_raw_data.frame_count()
    window_length = int(0.1 * framerate) # 与浏览器录音方式对齐，帧长100ms

    #  python2.7 division, float to int--round down
    energy = []
    for i in xrange(int(len(wave_data) / window_length)):
        # energy
        win_data = wave_data[window_length * i: window_length * (i + 1)]
        win_data_flo = np.array(win_data, dtype=np.float)
        en = (np.dot(win_data_flo, win_data_flo.T))
        if en < 0:
            print win_data_flo
            exit()
        energy.append(np.sqrt(en))

    i = 0
    # len(energy) is equal to len(data)/window_length
    active = False
    left_point = 0
    right_point = 0
    silence_counter = 0 #2018.8.13，静音帧统计
    audio_counter = 0 #2018.8.13，valid audio frame counter
    silence_trigger = True #2018.8.13，用于静音触发
    audio_trigger = False  #2018.8.13，用于语音触发
    enter_trigger = False  #2018.8.13，用于静音触发换行
    counter_enter = 0 #2018.8.13,统计静音时间计数，用来换行
    while i < len(energy):
        # energy
        active = audio_detection(energy[i])
        if active:
            silence_counter = 0
            audio_counter += 1
            if audio_counter >= 5 and (not audio_trigger):
                if i - 6 > 0:
                    left_point = i - 6
                silence_trigger = False
                audio_trigger = True
                enter_trigger = False
        else:
            audio_counter =0
            silence_counter += 1
            if i == len(energy) - 1:
                splited_audio = wave_data[left_point * window_length: ]
                splited_list.append(splited_audio)
                return splited_list
            if silence_counter >= 8 and (not silence_trigger): #如果静音0.8s，则认为说话结束
                if (i - left_point) > 10:
                    silence_trigger = True
                    audio_trigger = False
                    enter_trigger = True
                    right_point = i
                    splited_audio = wave_data[left_point * window_length : right_point * window_length]
                    splited_list.append(splited_audio)
                    silence_counter = 0
                    counter_enter =7

        if silence_trigger and enter_trigger:
            counter_enter += 1
            if counter_enter > 50 and enter_trigger: # 如果静音超过5秒，就换行，1s=10
                splited_list.append('return')
                enter_trigger = False
        i += 1
    return splited_list



    #     if energy[i] > E1:
    #         left_window_point = i
    #         enter_num = 0
    #         enter_trigger = True
    #         right_window_point = get_right_point(left_window_point, energy)
    #         if right_window_point == None:
    #             splited_audio = wave_data[(left_window_point-1) * window_length:]
    #             splited_list.append(splited_audio)
    #             return splited_list
    #         else:
    #             splited_audio = wave_data[(left_window_point-1) * window_length:(right_window_point+1) * window_length]
    #             splited_list.append(splited_audio)
    #         i = right_window_point
    #     else:
    #         enter_num += 1
    #         if enter_trigger and enter_num > 8:
    #         # 检测时间较长的静音段，用于换行。
    #             splited_list.append("return")
    #             enter_trigger = False
    #         i = i + 1
    # return splited_list

