import picamera
import time
import os
import sys 
import contextlib
from mqtt import *
from pathlib import Path
class Camera():
    #inittializing thread
    def __init__(self):
        data_files = 0
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.data_files = 0
        self.format = ".h264"
        self.mqttClient = connect_mqtt()
    
    def start(self):
        #count number of files in Data storage for footage file naming
        for files in os.walk("Data"):
            self.data_files += 1
        #create footage name
        abs_path = os.path.abspath('../Data')
        footage_path = os.path.join(abs_path, str((self.data_files+1)) + self.format)
        if not os.path.exists(footage_path):
            open(footage_path, 'w')
        #start recording
        self.camera.start_recording(footage_path)

        
    #run thread and record
    def stop(self):
        #reset file numbers
        self.data_files = 0
        #stop recording
        self.camera.stop_recording()
