import os
from mqtt import *
from static_detect import *
import time

detector = MotionDetector(2.5, 32)
time.sleep(5)
detector.scan(25)
time.sleep(10)
print("can do some stuff in between scans")
detector.scan(25)


