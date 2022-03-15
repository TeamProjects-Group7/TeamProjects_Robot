import picamera
import time
import os

def Record():
    camera = picamera.PiCamera()
    #camera is upside down by default apparently
    camera.vflip = True
    data_files = 0
    for files in os.walk("Data"):
        data_files += 1
    footage_name = "Data/Footage" + (data_files+1)
    camera.start_recording(footage_name)
    time.sleep(300)
    camera.stop_recording()
