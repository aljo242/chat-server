from server import *
from client import *
import time
import threading

clientIDs = [1, 2, 3]

def alexClient():
    alex = Client(1, "Alex")
    alex.sendWithName("Whats up!")
    time.sleep(10)

    alex.sendWithName("exit")

def sarahClient():
    time.sleep(10)
    sarah = Client(2, "Sarah")
    sarah.sendWithName("Hi Alex!")

    sarah.sendWithName("exit")

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, daemon= False)

    alexThread = threading.Thread(target = alexClient)
    sarahThread = threading.Thread(target = sarahClient)

    serverThread.start()
    time.sleep(1)
    alexThread.start()
    sarahThread.start()

