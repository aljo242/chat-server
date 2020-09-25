import socket
import threading 
import time
from _common_ import *


class Server:

    def __init__(self, clientIDs: list):
        self.clientIDs = clientIDs
        self.messageHistory = ["Welcome to the chatroom!"]
        self.connections = {}
        
        # create connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)

        # threading lock to ensure atomic access to connections
        self.lock = threading.Lock()

    def handleClient(self, connection, address):
        print(f"[NEW CONNECTION]: {address} connected")
        recievedID = False
        ID = 0

        while True:
            message = self.recv(connection)

            # print all recieved messages and send AK message to client
            print(f"[ID: {ID}] | message = {message}")
            
            if not recievedID:
                recievedID = True
                ID = int(message)
                #if ID is valid, add to our connections list
                if ID not in self.clientIDs:
                    # do nothing in this loop if connection is not in the trusted ID list
                    self.nonClientLoop()
                else:
                    self.connections[ID] = connection  
                
            elif message == MESSAGE_HISTORY_UPDATE_REQUEST:
                self.sendMessageHistory(connection)
                continue

            elif message == DISCONNECT_MESSAGE:
                print(f"[{ID}]: DISCONNECTING")
                print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 2}") # show that we have 1 less connection 
                break

            elif message == SERVER_AK_MESSAGE:
                continue

            # only append if the message is "of consequence"
            # use lock to ensure messageHistory atomically updated
            else: 
                self.lock.acquire()
                self.messageHistory.append(message)
                self.lock.release()

                self.dispatchMessage(ID, message)
            

    
        # handle disconnection
        del self.connections[ID]
        connection.close()

    def nonClientLoop(self):
        while True:
            pass

    # update message history for a client
    # send length of history to client
    # send each message
    def sendMessageHistory(self, connection):
        if len(self.messageHistory) != 0:
            print(f"Sending message history of length: {len(self.messageHistory)} ")
            self.send(connection, str(len(self.messageHistory)))

            for message in self.messageHistory:
                self.send(connection, message)


    def send(self, connection, message: str):
        message = message.encode(ENCODE_FORMAT)
        connection.send(message)
        self.recvAK(connection)

    def recvAK(self, connection):
        ak = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        if ak != SERVER_AK_MESSAGE:
            print("error with AK")

    def recvAndAK(self, connection):
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        # send AK message
        print("sending AK")
        connection.send(SERVER_AK_MESSAGE.encode(ENCODE_FORMAT))
        return message
        
    def recv(self, connection):
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        return message

    # send to all IDs except the origin ID (original sender of message)
    def dispatchMessage(self, originID: int, message: str):
        for ID in self.connections.keys():
            if ID != originID:
                print(f"sending from {originID} to {ID}")

                connection = self.connections[ID]
                self.send(connection, message)

    def start(self):
        self.server.listen() # listen for new connections
        print("Listening for connections...")
        while True:     # run until we quit
            # block at this line until new connection
            # after connecting, dispatch to a thread to handle in parallel
            connection, address = self.server.accept()
            thread = threading.Thread(target = self.handleClient, args = (connection, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}") # all non-master threads

    def run(self):
        print(f"Initializing server at port: {PORT} and IPv4: {SERVER}...")
        self.start()



if __name__ == "__main__":
    server = Server([1, 2, 3])
    server.run()
