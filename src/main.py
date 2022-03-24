from paho.mqtt.client import MQTTMessage
from mqtt import *
from MotionDetector import *
import time

idle = True
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

def main():
    global idle

    #rather than looping here we will probably check
    #"idle" at various points in the application and
    #exit main if its true
    while idle == False:
        print("Robot will function while idle is off")
        time.sleep(5)


subscriber = subscribe(set_idle, Topic.ROBOT_IDLE);
while True:
    while idle:
        print("Currently idle. Waiting...")
        time.sleep(5)

    main()