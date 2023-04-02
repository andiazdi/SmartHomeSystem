import asyncio
import random
import time
from datetime import datetime

from paho.mqtt import client as mqtt_client

from config import *


class MqttClient:
    def __init__(self, username, db):
        self.broker = mqtt_ip
        self.port = mqtt_port
        self.topic = topic
        self.client_id = f"python-mqtt-{random.randint(0, 1000)}"
        self.username = username
        # password = 'RFID'
        self.client = mqtt_client.Client(self.client_id)  # create new instance
        self.client.connect(self.broker)  # connect to broker

        self.db = db

    def make_message(self, from_username, to_username, cmd, user_id, payload="_"):
        ans = f"{from_username}|{to_username}|{user_id}|{cmd}|{payload}"
        return ans

    async def publish(self, message):
        self.client.publish(self.topic, message)  # publish

    async def get_all_connected_devices(self, user_id):
        msg = self.make_message("server", "all", "ping", user_id)

        await self.publish(msg)
        await asyncio.sleep(0.3)
        ans = await self.db.last_pinged_devices(user_id)
        return ans

    async def get_data_from_device(self, device_username, user_id):
        msg = self.make_message("server", device_username, "get_data", user_id)
        await self.publish(msg)
        await asyncio.sleep(0.5)
        ans = await self.db.select_data_from_device(device_username, user_id)
        return ans
