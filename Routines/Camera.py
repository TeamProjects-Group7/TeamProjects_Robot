import picamera
import time
import os
import threading
data_files = 0
camera = picamera.PiCamera()
alert = 0
lock = threading.Condition()
class Camera(threading.Thread()):
    #inittializing thread
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        camera.vflip = True
        data_files = 0
        for files in os.walk("Data"):
            data_files += 1
    #run thread and record
    def run(self):
        global alert
        footage_name = "Data/Footage" + (data_files+1)
        camera.start_recording(footage_name)
        while (alert):
            time.sleep(5)
        camera.stop_recording()
