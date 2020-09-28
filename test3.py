from server import *
from client import *
import time
import threading
import os


clientIDs = [1, 2, 3]

def alexClient():
    alex = Client(1, "Alex", os.path.join(PWD, "alex_test3.log"))
    alex.sendWithName("Whats up!")
    time.sleep(1)
    alex.sendWithName("Hey, got to go, bye!")

    alex.sendWithName("exit")
    time.sleep(1)
    alex.logMessageHistory() # debug log message history to show output that client would see

def sarahClient():
    time.sleep(10)
    sarah = Client(2, "Sarah", os.path.join(PWD, "sarah_test3.log"))
    sarah.sendWithName("Hi Alex!")

    sarah.sendWithName("exit")
    time.sleep(1)
    sarah.logMessageHistory() # debug log message history to show output that client would see

def bobClient():
    time.sleep(10)
    bob = Client(3, "Bob", os.path.join(PWD, "bob_test3.log"))
    bob.sendWithName("Hi Alex!")

    bob.sendWithName("exit")
    time.sleep(1)
    bob.logMessageHistory() # debug log message history to show output that client would see

def daveClient():
    dave = Client(4, "Dave", os.path.join(PWD, "dave_test3.log"))
    dave.sendWithName("Hi Alex!")
    time.sleep(5)
    dave.sendWithName("exit")
    time.sleep(1)
    dave.logMessageHistory() # debug log message history to show output that client would see

if __name__ == "__main__":
    serverThread = threading.Thread(target = runServer, args = [clientIDs, os.path.join(PWD, "server_test3.log")])

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

