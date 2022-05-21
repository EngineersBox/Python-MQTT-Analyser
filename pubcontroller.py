import time, threading
from connection.subscriber import Subscriber
from connection.publisher import Publisher

RESPONSE_TOPIC = "response/{qos}/{delay}"
REQUEST_TOPIC = "request"
REQUEST_QOS = 2
FILLER_MSG = "filler"

CLIENT_ID = "pubcontroller"
HOSTNAME = "localhost"
PORT = 1883

qos = None
delay = None
topic = None

def subscribeHandler(msg: str):
    global qos
    global delay
    global topic
    msgParts = msg.split('/')
    if (len(msgParts) != 3):
        raise RuntimeError(f"Message was not in expected format: response/qos/delay != {msg}")
    qos = int(msgParts[1])
    delay = int(msgParts[2])
    topic = msg
    print(f"Got request: {msg}")

def send(pub: Publisher):
    localCmp = None
    while True:
        if (localCmp != topic):
            localCmp = topic
        # print(f"SENDING: {topic}")
        if (qos == None or delay == None or topic == None):
            continue
        pub.publish(topic, qos, FILLER_MSG)
        time.sleep(delay / 1000)

def main():
    sub = Subscriber(f"{CLIENT_ID}-sub", HOSTNAME, PORT)
    pub = Publisher(f"{CLIENT_ID}-pub", HOSTNAME, PORT)

    pubThread = threading.Thread(target=send, args=[pub])
    pubThread.setDaemon(True)
    pubThread.start()

    sub.registerSubscribeEventHandler(lambda mc, u, msg: subscribeHandler(msg.payload.decode("utf-8")))
    sub.subscribe(REQUEST_TOPIC, REQUEST_QOS)

if __name__ == "__main__":
    main()
