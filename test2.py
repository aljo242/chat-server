from server import *
from client import *
import time
import threading

clientIDs = [1, 2, 3]

def alexClient():
    alex = Client(1, "Alex")
    time.sleep(2)
    alex.sendWithName("Whats up!")
    time.sleep(2)
    alex.sendWithName("Hey, got to go, bye!")

    alex.sendWithName("exit")
    time.sleep(1)
    alex.logMessageHistory("alex_test2") # debug log message history to show output that client would see

def sarahClient():
    sarah = Client(2, "Sarah")

    time.sleep(6)
    sarah.sendWithName("exit")
    time.sleep(1)
    sarah.logMessageHistory("sarah_test2") # debug log message history to show output that client would see

def bobClient():
    bob = Client(3, "Bob")

    time.sleep(6)
    bob.sendWithName("exit")
    time.sleep(1)
    bob.logMessageHistory("bob_test2") # debug log message history to show output that client would see

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, daemon= False)

    alexThread = threading.Thread(target = alexClient)
    sarahThread = threading.Thread(target = sarahClient)
    bobThread = threading.Thread(target = bobClient)

    serverThread.start()
    time.sleep(1)
    alexThread.start()
    sarahThread.start()
    bobThread.start()

