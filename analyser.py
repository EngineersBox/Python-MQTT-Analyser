from time import sleep
from connection.subscriber import Subscriber
from connection.publisher import Publisher
import threading

RESPONSE_TOPIC = "response/{qos}/{delay}"
REQUEST_TOPIC = "request"
REQUEST_QOS = 2

TESTING_LEVELS = [0, 1, 2]
TESTING_DELAYS = [0, 10, 20, 50, 100, 500]

CLIENT_ID = "analyser"
HOSTNAME = "localhost"
PORT = 1332

results = {}

def subscribeHandler(delay: int, qos: int):
    global results
    results[f"{delay}/{qos}"] += 1
    # print(f"response: {delay} {qos}")

def main():
    global results
    sub = Subscriber(f"{CLIENT_ID}-sub", HOSTNAME, PORT)
    pub = Publisher(f"{CLIENT_ID}-pub", HOSTNAME, PORT)

    for qos in TESTING_LEVELS:
        print(f"Sending {qos} {TESTING_DELAYS}")
        for delay in TESTING_DELAYS:
            results[f"{delay}/{qos}"] = 0
            sub.registerSubscribeEventHandler(lambda mc, u, ms: subscribeHandler(delay, qos))
            pub.registerPublishEventHandler(lambda mc, u, ms: sub.subscribe(RESPONSE_TOPIC.format(qos=qos, delay=delay), qos))

            pubThread = threading.Thread(target=pub.publish, args=[REQUEST_TOPIC, qos, RESPONSE_TOPIC.format(qos=qos, delay=delay)])
            pubThread.setDaemon(True)
            pubThread.start()
            sleep(40 * (qos + 1))
            sub.disconnect()
            sub.connect()
            print(results)

    sub.disconnect()
    pub.disconnect()

if __name__ == "__main__":
    main()
