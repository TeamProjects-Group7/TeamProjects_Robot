import pyaudio
import wave
import os

class Microphone:
    def __init__(self):
        self.is_recording = False
        self.pyaudio = pyaudio.PyAudio()

    def __del__(self):
        if self.is_recording:
            self.stop_recording()
    
    def get_filename():
        data_files = 0
        for files in os.walk("Data"):
            data_files += 1
        return "Data/Audio" + (data_files+1)

    def start_recording(self):
        if self.is_recording:
            return

        self.wav_file = wave.open(self.get_filename, 'rb')
        
        def callback(in_data, frame_count, time_info, status):
            data = self.wav_file.readframes(frame_count)
            return (data, pyaudio.paContinue)

        self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.wav_file.getsampwidth()),
                channels=self.wav_file.getnchannels(),
                rate=self.wav_file.getframerate(),
                output=True,
                stream_callback=callback)
        self.stream.start_stream()
        

    def stop_recording(self):
        if not self.is_recording:
            return
        self.stream.stop_stream()
        self.stream.close()
        self.wav_file.close()
