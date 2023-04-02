import paho.mqtt.client as mqtt
import requests

from config import *
from db.db import *

devices_db = Devices()


def on_connect(client, userdata, flags, rc):
    print(f"{bcolors.OKGREEN}Connected with result code {rc}{bcolors.ENDC}")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    from_username, to_username, user_id, cmd, payload = msg.payload.decode().split('|')
    device_data = devices_db.insert_device(
        from_username, to_username, user_id, cmd, payload
    )  
    if from_username != "server":
        print(
            f"{bcolors.HEADER}Message"
            f" received -> {msg.topic} {bcolors.OKCYAN}{msg.payload}{bcolors.ENDC}"
        )


client = mqtt.Client(
    "digi_mqtt_test"
)  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_ip, mqtt_port)


client.loop_forever()
