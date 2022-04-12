from paho.mqtt.client import MQTTMessage
from mqtt import *
from MotionDetector import *
import time
from Camera import *
from Microphone import *
from DataTransfer.TransferFiles import *

idle = True
alerted = False
camera = Camera()
mic = Microphone()

def set_idle(client, userdata, msg: MQTTMessage):
    global idle
    status = msg.payload.decode().lower()
    if(status != "false" and status != "true"):
        return;

    if status == "false":
        idle = False
    else:
        idle = True
    print(f"Set idle state to {idle}\n")

def on_alert_off(client, userdata, msg:MQTTMessage):
    camera.stop()
    mic.stop_recording()
    #upload all files to github
    alerted = False

def raise_alert(publisher):
    alerted = True
    publish(publisher, "", Topic.ALERT_ON)
    camera.start()
    mic.start_recording()
    count = 0
    while(alerted & count <= 100):
        time.sleep(5)
        count = count + 1
    if(count >= 100):
        camera.stop()
        mic.stop_recording()
        #upload all files to github
        alerted = False


def main():
    global idle
    global alerted
    #rather than looping here we will probably check
    #"idle" at various points in the application and
    #exit main if its true
    while idle == False:
        print("Robot will function while idle is off")
        if (mic.idleListen() > 20):
            raise_alert(publisher)


subscriber = subscribe(set_idle, Topic.ROBOT_IDLE);
publisher = getClient()

while True:
    while idle:
        print("Currently idle. Waiting...")
        time.sleep(5)
       
            
            


    main()