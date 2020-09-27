import socket
from _common_ import *
import argparse
import threading
import time

class Client:
    def __init__(self, ID: int, name: str):
        self.clientIDs = []
        self.name = name
        self.ID = ID
        self.messageHistory = []
        self.kill = False

        self.lock = threading.Lock()

        # connect to server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(ADDRESS)

        # send ID to server and recieve message history
        self.send(str(self.ID))
        self.updateMessageHistory()

        reciever = threading.Thread(target = self.recieveLoop, daemon = True)
        reciever.start()
        self.run()

    # recieving loop to be executed as a thread
    def recieveLoop(self):
        while True:
            if self.kill:
                break

            message = self.recv(self.connection)
            if message != SERVER_AK_MESSAGE:   # filter messages to be printed to client
                print(message)

    # main loop which takes user input and sends to the server
    # recieve loop runs in parallel as a thread
    def run(self):
        while True:
            message = input()
            if message == CLIENT_EXIT_MESSAGE:
                break
            
            self.sendWithName(message)

        self.disconnect()

    # clean up operations and message to server to disconnect cleanly
    def disconnect(self):
        self.kill = True # use this to kill reciever loop
        print("disconnecting...")
        self.send(DISCONNECT_MESSAGE)
        time.sleep(1) # simulate some kind of server xaction
        self.connection.close()
        print("disconnected.")

    def send(self, message: str):
        if message == CLIENT_EXIT_MESSAGE:
            self.disconnect()
        else:
            message = message.encode(ENCODE_FORMAT)
            self.connection.send(message)
            time.sleep(.05) # simulate latency

    def sendWithName(self, message: str):
        if message == CLIENT_EXIT_MESSAGE:
            self.disconnect()
        else:
            message = f"[{self.name}]: " + message
            self.send(message)
    
    def recv(self, connection):
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        return message

    def recvAndAK(self, connection):
        message = self.recv(connection)
        connection.send(SERVER_AK_MESSAGE.encode(ENCODE_FORMAT))
        return message
            
    def updateMessageHistory(self):
        self.send(MESSAGE_HISTORY_UPDATE_REQUEST)
        numMessages = int(self.recvAndAK(self.connection))
        for _ in range(numMessages):
            self.messageHistory.append(self.recvAndAK(self.connection))

        for message in self.messageHistory:
            print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id")
    parser.add_argument("name")

    args = parser.parse_args()

    myClient = Client(args.id, args.name)