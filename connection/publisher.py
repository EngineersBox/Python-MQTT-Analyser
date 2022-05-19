from typing import Any, Callable
import paho.mqtt.client as mqtt

MESSAGE_HANDLER_TYPE = Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]

class Publisher:

    def __init__(self, client_id: str, host: str, port: int):
        self.client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv311,
            clean_session=True
        )
        self.client.connect(host, port, 60)

    def registerPublishEventHandler(self, onPublish: MESSAGE_HANDLER_TYPE):
        self.client.on_publish = onPublish

    def publish(self, topic: str, qos: int, msg: Any):
        msgInfo: mqtt.MQTTMessageInfo = self.client.publish(topic, msg, qos)
        if (msgInfo.rc == mqtt.MQTT_ERR_NO_CONN):
            raise RuntimeError("Client not connected")
        msgInfo.wait_for_publish()
    
    def disconnect(self):
        self.client.disconnect()
