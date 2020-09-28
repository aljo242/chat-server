from server import *
from client import *
import time
import threading
import os
import sys

clientIDs = [1, 2]

def alexClient():
    alex = Client(1, "Alex", os.path.join(PWD, "alex_test1.log"))
    alex.sendWithName("Whats up!")
    time.sleep(5)
    alex.sendWithName("Hey, got to go, bye!")

    alex.sendWithName("exit")
    time.sleep(10)

    alex = Client(1, "Alex", os.path.join(PWD, "alex_test1.log"))
    alex.sendWithName("exit")

    alex.logMessageHistory() # debug log message history to show output that client would see

def sarahClient():
    time.sleep(10)
    sarah = Client(2, "Sarah", os.path.join(PWD, "sarah_test1.log"))
    sarah.sendWithName("Hi Alex!")

    sarah.sendWithName("exit")
    time.sleep(1)
    sarah.logMessageHistory() # debug log message history to show output that client would see

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, args = [clientIDs, os.path.join(PWD, "server_test1.log")], daemon = False )

    alexThread = threading.Thread(target = alexClient, daemon= False)
    sarahThread = threading.Thread(target = sarahClient, daemon= False)

    serverThread.start()
    time.sleep(1)
    alexThread.start()
    sarahThread.start()


