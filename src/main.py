import os
from mqtt import *

def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

subscriber = subscribe(on_message, Topic.ALERT_ON)

publisher = getClient()
publish(publisher, "", Topic.ALERT_ON)
publish(publisher, "test message", Topic.ALERT_ON)
publish(publisher, "an alert happened", Topic.ALERT_ON)