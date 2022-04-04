import picamera
import time
import os
import sys 
import contextlib
from paho.mqtt.client import MQTTMessage
from mqtt import *
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
        footage_name = "Data/Footage" + (self.data_files+1) + self.format
        open(footage_name)
        #start recording
        self.camera.start_recording(footage_name)

        
    #run thread and record
    def stop(self):
        #reset file numbers
        self.data_files = 0
        #stop recording
        self.camera.stop_recording()
