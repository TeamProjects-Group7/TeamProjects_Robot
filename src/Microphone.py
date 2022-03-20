import pyaudio
import wave
import os

class Microphone:
    def __init__(self):
        self.is_recording = False
        with ignoreStderr():
            self.pyaudio = pyaudio.PyAudio()

    def __del__(self):
        if self.is_recording:
            self.stop_recording()
    
    def get_new_filename(self):
        path, dirs, files = next(os.walk("../Data/Audio"))
        file_count = len(files)
        filename = "../Data/Audio/" + str((file_count+1)) + ".wav"
        filename = os.path.abspath(filename)
        open(filename, "x")
        return filename

    def start_recording(self):
        if self.is_recording:
            return

        # file = self.get_new_filename()
        # self.wav_file = wave.open(file, 'rb')
        
        # def callback(in_data, frame_count, time_info, status):
        #     data = self.wav_file.readframes(frame_count)
        #     return (data, pyaudio.paContinue)

        # self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.wav_file.getsampwidth()),
        #         channels=self.wav_file.getnchannels(),
        #         rate=self.wav_file.getframerate(),
        #         output=True,
        #         stream_callback=callback)

        # self.stream.start_stream()

        sample_format = pyaudio.paInt16 
        chanels = 2
        smpl_rt = 44400 
        seconds = 4
        chunk = 1024 
        self.stream = self.pyaudio.open(format=sample_format, channels=chanels,
                 rate=smpl_rt , input=True,
                 frames_per_buffer=chunk)

        print('Recording...')
        frames = []

        for i in range(0, int(smpl_rt / chunk * seconds)):
            data = self.stream.read(chunk)
            frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()
        
        self.pyaudio.terminate()
        
        print('Done !!! ')
        
        sf = wave.open('/home/pi/Development/TeamProjects_Robot/Data/Audio/1.wav', 'wb')
        sf.setnchannels(chanels)
        sf.setsampwidth(self.pyaudio.get_sample_size(sample_format))
        sf.setframerate(smpl_rt)
        sf.writeframes(b''.join(frames))
        sf.close()
        

    def stop_recording(self):
        if not self.is_recording:
            return
        self.stream.stop_stream()
        self.stream.close()
        self.wav_file.close()

import time, os, sys, contextlib

#pyaudio.PyAudio displays some debug messages which
#are extra noise. We use this to hide the messages.
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