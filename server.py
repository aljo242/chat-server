import socket
import threading
import time
from _common_ import *
import logging

class Server:
    def __init__(self, clientIDs: list):
        # init logging
        logging.basicConfig(filename = "server.log", filemode = 'w',
            format='%(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)
        
        self.clientIDs = clientIDs
        self.messageHistory = [CHATROOM_WELCOME_MESSAGE]
        self.nonClientMessage = [CHATROOM_NON_CLIENT_MESSAGE]
        self.connections = {}

        # create connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)

        # threading lock to ensure atomic access
        self.lock = threading.Lock()

    def handleClient(self, connection, address):
        logging.debug(f"[NEW CONNECITON]: {address}")
        recievedID = False
        ID = 0

        while True:
            message = self.recv(connection)

            # print all recieved messages to log
            logging.debug(f"[ID: {ID}] message = {message}")

            # clients are required to first send their ID to server
            if not recievedID:
                recievedID = True
                ID = int(message)
                # if ID is in list of clients to add, add connection
                if ID in self.clientIDs:
                    self.connections[ID] = connection
                continue

            elif message == MESSAGE_HISTORY_UPDATE_REQUEST:
                self.sendMessageHistory(connection, ID)
                continue

            elif message == DISCONNECT_MESSAGE:
                logging.debug(f"[{ID}] DISCONNECTING")

                # remove from our connections list, so we won't broadcast 
                # message to it after disconnection
                if ID in self.clientIDs:
                    del self.connections[ID]
                connection.send(SERVER_AK_MESSAGE.encode(ENCODE_FORMAT))
                break
            
            # only append the message history if it is one 
            # we "care about"
            # use lock so it is atomically updated
            else:
                # if client is not permitted, do not record messages
                if ID in self.clientIDs:
                    self.lock.acquire()
                    self.messageHistory.append(message)
                    self.lock.release()

                    self.dispatchMessage(ID, message)
                
        logging.debug("exiting thread handler...")

    # update message history 
    # all clients recieve message history when connecting to server
    def sendMessageHistory(self, connection, ID: int):
        messagesToSend = []
        if ID in self.clientIDs:
            messagesToSend = self.messageHistory
        else:
            messagesToSend = self.nonClientMessage

        # send client the number of messages we are going to send,
        # then send the actual message
        if len(self.messageHistory) != 0:
            logging.debug(f"Sending message history of length: {len(messagesToSend)}")
            self.send(connection, str(len(messagesToSend)))

            for message in messagesToSend:
                self.send(connection, message)

    def send(self, connection, message: str):
        self.sendNoAK(connection, message)
        self.recvAK(connection)

    def sendNoAK(self, connection, message: str):
        message = message.encode(ENCODE_FORMAT) 
        connection.send(message)

    # recieve AK message from recipient of "SEND" operation
    def recvAK(self, connection):
        ak = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        if ak != SERVER_AK_MESSAGE:
            logging.debug("Error getting AK")

    def recv(self, connection):
        message = connection.recv(MAX_MESSAGE_BYTES).decode(DECODE_FORMAT)
        return message

    # broadcast to IDs except the origin ID (original sender)
    def dispatchMessage(self, originID: int, message: str):
        for ID in self.connections.keys():
            if ID != originID:
                logging.debug(f"sending from {originID} to {ID}")

                connection = self.connections[ID]
                self.sendNoAK(connection, message)
    
    def start(self):
        self.server.listen() # listen for new connections
        logging.debug("Listening for connections...")
        while True: # run until quit
            # block until new connection
            connection, address = self.server.accept()
            thread = threading.Thread(target = self.handleClient, args = (connection, address))
            thread.start()
            # print totalThreads - 1 since 
            # master thread handling dispatching new connections
            logging.debug(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")

    def run(self):
        logging.debug(f"Initializing server at port: {PORT}, and IPv4: {SERVER}....")
        self.start()

def runServer():
    server = Server([1, 2, 3])
    server.run()

if __name__ == "__main__":
    runServer()