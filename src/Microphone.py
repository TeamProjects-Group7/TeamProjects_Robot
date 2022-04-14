import pyaudio
import wave
import os
import time
import sys 
import contextlib
from paho.mqtt.client import MQTTMessage
from mqtt import *
import struct
import math
#Constants

def getAmplitude(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        # normalize samples
        n = sample * (1.0/32768.0)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

class Microphone:
    def __init__(self):
        self.is_recording = False
        self.format = pyaudio.paInt16 
        self.channels = 2
        self.framerate = 44400 
        self.chunk = 1024
        with ignoreStderr():
            self.pyaudio = pyaudio.PyAudio()
        self.mqttClient = connect_mqtt()

    def __del__(self):
        if self.is_recording:
            self.stop_recording()
    
    def get_audio_file(self):
        path, dirs, files = next(os.walk("../Data"))
        file_count = len(files)
        filename = "../Data" + str((file_count+1)) + ".wav"
        filename = os.path.abspath(filename)
        open(filename, "x")
        return filename
    
    def open_wave_file(self, filename):
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.pyaudio.get_sample_size(self.format))
        wave_file.setframerate(self.framerate)
        return wave_file

    def start_recording(self):
        if self.is_recording:
            return

        self.is_recording = True

        filename = self.get_audio_file()
        self.wave_file = self.open_wave_file(filename)

        def callback(in_data, frame_count, time_info, status):
            self.wave_file.writeframes(in_data)
            return in_data, pyaudio.paContinue

        self.stream = self.pyaudio.open(format=self.format, 
            channels=self.channels,
            rate=self.framerate, 
            input=True,
            frames_per_buffer=self.chunk, 
            stream_callback=callback)        
        self.stream.start_stream()              

    def stop_recording(self):
        if not self.is_recording:
            return
        self.stream.stop_stream()
        self.stream.close()
        self.wave_file.close()
        self.is_recording = False
    
    def idleListen(self):
        alerted = False
        stream = self.pyaudio.open(
        format=self.format,
        channels=self.channels,
        rate=self.framerate,
        input=True,
        output=True,
        frames_per_buffer=self.chunk*2.0
        )
        micData = stream.read(self.chunk)
        amplitude = getAmplitude(micData)
        decibels = 20*math.log10(amplitude)
        return decibels

#pyaudio.PyAudio displays some debug messages which
#aren't helpful to see. We use this to hide the messages.
@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)