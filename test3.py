from server import *
from client import *
import time
import threading

clientIDs = [1, 2, 3]

def alexClient():
    alex = Client(1, "Alex")
    alex.sendWithName("Whats up!")
    time.sleep(1)
    alex.sendWithName("Hey, got to go, bye!")

    alex.sendWithName("exit")
    time.sleep(1)
    alex.logMessageHistory("alex_test2") # debug log message history to show output that client would see

def sarahClient():
    time.sleep(10)
    sarah = Client(2, "Sarah")
    sarah.sendWithName("Hi Alex!")

    sarah.sendWithName("exit")
    time.sleep(1)
    sarah.logMessageHistory("sarah_test2") # debug log message history to show output that client would see

def bobClient():
    time.sleep(10)
    bob = Client(3, "Bob")
    bob.sendWithName("Hi Alex!")

    bob.sendWithName("exit")
    time.sleep(1)
    bob.logMessageHistory("bob_test2") # debug log message history to show output that client would see

def daveClient():
    dave = Client(4, "Dave")
    dave.sendWithName("Hi Alex!")
    time.sleep(5)
    dave.sendWithName("exit")
    time.sleep(1)
    dave.logMessageHistory("dave_test2") # debug log message history to show output that client would see

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, daemon= False)

    alexThread = threading.Thread(target = alexClient)
    sarahThread = threading.Thread(target = sarahClient)
    bobThread = threading.Thread(target = bobClient)
    daveThread = threading.Thread(target = daveClient)

    serverThread.start()
    time.sleep(1)
    alexThread.start()
    sarahThread.start()
    bobThread.start()
    daveThread.start()

