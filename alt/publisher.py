import paho.mqtt.client as mqtt

class Publisher():

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = Publisher.on_connect
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(mqttc, obj, flags, rc):
        print("Connected: " + str(rc))

    def publish(self, topic, msg, qos):
        res = self.client.publish(topic, msg, qos=qos)
        res.wait_for_publish()
