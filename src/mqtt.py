# python3.6

import random
from enum import Enum
from paho.mqtt import client as mqtt_client

class Topic(Enum):
    ALERT_ON = 1
    ALERT_OFF = 2
    ROBOT_IDLE = 3

broker = 'broker.emqx.io'
port = 1883
username = 'group7robot'
password = 'thisisntsecureohwell'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(client, userdata, flags, rc):
        print("Disconnected from MQTT Broker")

    client = mqtt_client.Client(f'python-mqtt-{random.randint(0, 100)}')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client

def getClient():
    client = connect_mqtt()
    client.loop_start()
    return client;

def subscribe(on_message, topic : Topic):
    if not callable(on_message):
        raise Exception("Subscriber must have a callback for on_message")
    client = connect_mqtt()
    client.on_message = on_message
    client.subscribe(str(topic))
    client.loop_start()
    return client

def publish(client: mqtt_client, msg : str, topic: Topic):
    result = client.publish(str(topic), msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send '{msg}' to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")
