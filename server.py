import socket
import threading 

# header begins each message
# is 8 bytes ( 64-bit),
# and tells server how long each message is in total 
MESSAGE_HEADER_BYTES = 8
MAX_MESSAGE_BYTES = 1024

# format to decode messages into bytes
DECODE_FORMAT = "utf-8"

# some unique message clients send server on disconnect
DISCONNECT_MESSAGE = "!DiScOnEcTeD!" 

PORT = 5050 # generic port to use
# automatically get host IP address
# use this to run server on
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

# use IPv4 
# streaming data
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handleClient(connection, address):
    print(f"[NEW CONNECTION]: {address} connected")

    while True:
        # blocking call - wait until recieve messaage
        # first recieve messageLength in fixed size header
        # then recieve the rest of the real message
        messageLength = int(connection.recv(MESSAGE_HEADER_BYTES).decode(DECODE_FORMAT))
        message = connection.recv(messageLength).decode(DECODE_FORMAT)
        if message == DISCONNECT_MESSAGE:
            break
        
        print(f"[{address}]: {message}")
    
    # handle disconnection
    connection.close()

def start():
    server.listen() # listen for new connections
    print("Listening for connections...")
    while True:     # run until we quit
         # block at this line until new connection
         # after connecting, dispatch to a thread to handle in parallel
        connection, address = server.accept()
        thread = threading.Thread(target = handleClient, args = (connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}") # all non-master threads

print(f"Initializing server at port: {PORT} and IPv4: {SERVER}...")
start()