
# coding: utf-8

# In[ ]:


## Plays audio from a .wav file
import pyaudio
import wave
import sys

class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        if (self.stream.is_active() == 0):
            self.stream.start_stream()

        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()
        
    def stop(self):
        """ Pauses stream """ 
        self.stream.stop_stream()
    def active(self):
        """ Check activeness """
        self.stream.is_active()

# Usage example for pyaudio
## Will play audio file until end.
a = AudioFile("coryhouse.wav") 		# Has 16-bit format
a.play()
a.stop()
a.active()

