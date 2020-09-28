from server import *
from client import *
import time
import threading
import os


clientIDs = [1, 2, 3]

def alexClient():
    alex = Client(1, "Alex", os.path.join(PWD, "alex_test2.log"))
    time.sleep(2)
    alex.sendWithName("Whats up!")
    time.sleep(2)
    alex.sendWithName("Hey, got to go, bye!")

    alex.sendWithName("exit")
    time.sleep(1)
    alex.logMessageHistory() # debug log message history to show output that client would see

def sarahClient():
    sarah = Client(2, "Sarah", os.path.join(PWD, "sarah_test2.log"))

    time.sleep(6)
    sarah.sendWithName("exit")
    time.sleep(1)
    sarah.logMessageHistory() # debug log message history to show output that client would see

def bobClient():
    bob = Client(3, "Bob", os.path.join(PWD, "bob_test2.log"))

    time.sleep(6)
    bob.sendWithName("exit")
    time.sleep(1)
    bob.logMessageHistory() # debug log message history to show output that client would see

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, args = [clientIDs, os.path.join(PWD, "server_test2.log")])

    alexThread = threading.Thread(target = alexClient)
    sarahThread = threading.Thread(target = sarahClient)
    bobThread = threading.Thread(target = bobClient)

    serverThread.start()
    time.sleep(1)
    alexThread.start()
    sarahThread.start()
    bobThread.start()

