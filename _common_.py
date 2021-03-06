# common values for server and client functionality
import logging
import socket
import os

PWD = os.getcwd()
print(PWD)

# header begins each message
# is 64 bytes
# and tells server how long each message is in total 
MESSAGE_HEADER_BYTES = 8
MAX_MESSAGE_BYTES = 1024

MAX_SERVER_RUNTIME_S = 20

# format to decode/encode messages into bytes
DECODE_FORMAT = "utf-8"
ENCODE_FORMAT = "utf-8"

# some unique message clients send server on disconnect
DISCONNECT_MESSAGE = "_!DiScOnEcTeD!_" 

# Server returns this message if successfully recieved
SERVER_AK_MESSAGE = "_ACK_"

# send message history update is sent
MESSAGE_HISTORY_UPDATE_REQUEST = "_MESSAGE_HISTORY_UPDATE_REQUEST_"
MESSAGE_HISTORY_UPDATE_COMPLETE = "_MESSAGE_HISTORY_UPDATE_COMPLETE_"

# message for clients to exit the chat room
CLIENT_EXIT_MESSAGE = "exit"
# message for cmd line on server side to shut down
SERVER_EXIT_MESSAGE = "exit"

# default chatroom welcome message
CHATROOM_WELCOME_MESSAGE = "Welcome to the chatroom!"

# default message for non-clients entering server
CHATROOM_NON_CLIENT_MESSAGE = "You are not permitted to join this chatroom!"

PORT = 5000 # generic port to use
# automatically get host IP address
# use this to run server on
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
