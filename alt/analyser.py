import subscriber, publisher, threading

def main():
    sub = subscriber.Subscriber()
    pub = publisher.Publisher()

    subThread = threading.Thread(target = lambda: sub.subscribe("result", 2))
    subThread.setDaemon(True)
    subThread.start()

    pub.publish("indicator", "prefix/result/2", 2)
    subThread.join()

if __name__ == "__main__":
    main()