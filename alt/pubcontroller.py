import subscriber, publisher, threading

def forwardAndPublish(msg, pub: publisher.Publisher):
    # print("Recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msgParts = msg.payload.decode("utf-8").split("/")
    print(f"Publishing to {msgParts[1]} at QoS {int(msgParts[2])}")
    for _ in range(0, 10):
        pub.publish(msgParts[1], f"Message sent to {msgParts[1]} @ {int(msgParts[2])}", int(msgParts[2]))

def subMethod(pub):
    sub = subscriber.Subscriber(lambda mq, o, msg: forwardAndPublish(msg, pub))
    sub.subscribe("indicator", 2)

def main():
    pub = publisher.Publisher()
    subThread = threading.Thread(target = lambda: subMethod(pub))
    subThread.setDaemon(True)
    subThread.start()
    subThread.join()

if __name__ == "__main__":
    main()