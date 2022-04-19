from paho.mqtt.client import MQTTMessage
from mqtt import *
#from MotionDetector import *
import time
from Camera import *
from Microphone import *
from TransferFiles import *
from Robot_Line_Follower import Robot_Line_Follower

idle = True
alerted = False
camera = Camera()
mic = Microphone()
mD = MotionDetector() 
publisher = getClient()
lf = Robot_Line_Follower()

def set_idle(client, userdata, msg: MQTTMessage):
    global idle
    status = msg.payload.decode().lower()
    if(status != "notidling" and status != "idling"):
        return

    if status == "not idling":
        idle = False
    else:
        idle = True
    print(f"Set idle state to {idle}\n")

def on_alert_off(client, userdata, msg:MQTTMessage):
    camera.stop()
    mic.stop_recording()
    #uploadAll()
    alerted = False

def raise_alert(publisher):
    alerted = True
    publish(publisher, "", Topic.ALERT_ON)
    camera.start()
    mic.start_recording()
    count = 0
    #Fix amount of count and time.sleep()
    #its longer than expected
    while(alerted & count <= 1):
        time.sleep(5)
        count = count + 1
        if(count >= 1):
            camera.stop()
            mic.stop_recording()
            #uploadAll()
            alerted = False

def main():
    global idle
    global alerted
    #rather than looping here we will probably check
    #"idle" at various points in the application and
    #exit main if its true
    while idle == False
        print("Robot will function while idle is off")
        lf.start()
        #put idle listen in a loop to check while robot is working
        if (mic.idleListen() >= -40):
            raise_alert(publisher)
        lf.stop()
        #stop for scanning
        if(mD.scan(1, False)):
            raise_alert(publisher)


subscribe(set_idle, Topic.ROBOT_IDLE.name)
while True:
    while idle:
        print("Currently idle. Waiting...")
        time.sleep(5)

    main()