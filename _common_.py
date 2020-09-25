# common values for server and client functionality
import socket

# header begins each message
# is 64 bytes
# and tells server how long each message is in total 
MESSAGE_HEADER_BYTES = 8
MAX_MESSAGE_BYTES = 1024

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

PORT = 5050 # generic port to use
# automatically get host IP address
# use this to run server on
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)