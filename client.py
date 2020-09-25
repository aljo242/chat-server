import socket
from _common_ import *
import argparse
import threading
import time


parser = argparse.ArgumentParser()
parser.add_argument("id")
parser.add_argument("name")

class client(threading.Thread):
    def __init__(self, ID: int, name: str):
        super().__init__(daemon=False, target = self.run)
        self.clientIDs = []
        self.messageHistory = []
        self.name =name
        self.ID = ID

        self.lock = threading.Lock()
        # connect
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(ADDRESS)
        
        #send connection info to server
        self.send(str(self.ID))

        self.updateMessageHistory()

        reciever = threading.Thread(target = self.recieve, daemon = True)
        reciever.start()
        self.start()

    def recieve(self):
        while True:
            message = self.recvAndAK(self.connection)
            
            if message != SERVER_AK_MESSAGE:
                print(message)

            time.sleep(.016)


    def run(self):
        while True:
            self.sendWithName(input())


    # automatically disconnect
    def __del__(self):
       self.send(DISCONNECT_MESSAGE)

    def send(self, message: str):
        message = message.encode(ENCODE_FORMAT)
        self.connection.send(message)
        time.sleep(.016)

    def recvAndAK(self, connection):
        # blocking call - wait until recieve messaage
        # first recieve messageLength in fixed size header
        # then recieve the rest of the real message
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        # send AK message
        connection.send(SERVER_AK_MESSAGE.encode(ENCODE_FORMAT))
        return message

    def recv(self, connection):
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        return message

    def sendWithName(self, message: str):
        message = f"[{self.name}]: " + message
        self.send(message)
        
    def updateMessageHistory(self):
        self.send(MESSAGE_HISTORY_UPDATE_REQUEST)
        numMessages = int(self.recvAndAK(self.connection))
        for _ in range(numMessages):
            self.messageHistory.append(self.recvAndAK(self.connection))
        
        for message in self.messageHistory:
            print(message)

if __name__ == "__main__":

    args = parser.parse_args()

    myClient = client(args.id, args.name) 

