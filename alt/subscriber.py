import paho.mqtt.client as mqtt

class Subscriber():

    def __init__(self, on_message=None):
        self.client = mqtt.Client()
        self.client.on_connect = Subscriber.on_connect
        self.client.on_message = Subscriber.internal_on_message if on_message == None else on_message
        self.client.connect("localhost", 1883, 60)

    def on_connect(mqttc, obj, flags, rc):
        print("Connected: " + str(rc))

    def internal_on_message(mqttc, obj, msg):
        print("Recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def subscribe(self, topic, qos):
        res = self.client.subscribe(topic, qos)
        self.client.loop_forever()
