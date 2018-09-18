2018.9.16,调整普天转写平台的语音端点检测算法，这次设置固定阈值
1.merge_audio.py:抽取静音音频，将几段静音音频整合为一段
  方法：pydub.AudioSegment
  input:几段短wav文件
  output:一段长wav文件

2.silence_estimate.py:估计一个固定静音阈值，在此基础上进行语音端点检测
  input:wav文件
  output:silence_value,能量计算公式：energy= np.sqrt(每帧向量的内积~np.dot(array,array.T))

3.speech_separation_energy.py：非实时语音端点检测：采用基于能量的双阈值门限方法
  2中的能量阈值作为低阈值
  
4.实时语音端点检测：采用基于能量的双阈值门限方法  
