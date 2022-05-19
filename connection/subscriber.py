from typing import Any, Callable
import paho.mqtt.client as mqtt

MESSAGE_HANDLER_TYPE = Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]

class Subscriber:

    def __init__(self, client_id: str, host: str, port: int):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.connect()

    def registerSubscribeEventHandler(self, onMessage: MESSAGE_HANDLER_TYPE):
        self.client.on_message = onMessage

    def subscribe(self, topic: str, qos: int):
        result, _ = self.client.subscribe(topic, qos)
        if (result == mqtt.MQTT_ERR_NO_CONN):
            raise RuntimeError("Client not connected")
        self.client.loop_forever()

    def connect(self):
        self.client = mqtt.Client(
            client_id=self.client_id,
            protocol=mqtt.MQTTv311,
            clean_session=True
        )
        self.client.connect(self.host, self.port, 60)

    def disconnect(self):
        self.client.disconnect()
