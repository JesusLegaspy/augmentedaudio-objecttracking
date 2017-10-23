
# coding: utf-8

# In[ ]:


import pyaudio
import time
import numpy as np
import scipy.signal as signal
import keyboard #Using module keyboard

WIDTH = 2
CHANNELS = 2
RATE = 44100
n = 10
p_mic = pyaudio.PyAudio()
b_mic,a_mic=signal.iirdesign(0.03,0.07,5,40)
fulldata = np.array([])
def callback(in_data, frame_count, time_info, flag):
    global b_mic,a_mic,fulldata #global variables for filter coefficients and array
    audio_data = np.fromstring(in_data, dtype=np.int16)
    #do whatever with data, in my case I want to hear my data filtered in realtime
    audio_data = signal.filtfilt(b_mic,a_mic,audio_data,padlen=200).astype(np.int16).tostring()
    fulldata = np.append(fulldata,audio_data) #saves filtered data in an array
    return (audio_data, pyaudio.paContinue)
stream_mic = p_mic.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream_mic.start_stream()
while True:
    if stream_mic.is_active():
        time.sleep(n)		# n seconds of audio, here, doing 30
        #print (fulldata)
        stream_mic.stop_stream()
    elif keyboard.is_pressed('o'):
        stream_mic.stop_stream()
    elif keyboard.is_pressed('p'):
        stream_mic.start_stream()
#stream_mic.close()

#p_mic.terminate()

