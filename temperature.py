import socket
import json
import time

SERVER = "192.168.68.114"
PORT = 1337 
HEADER = 8  
DISCONNECT_MSG = "!DISCONNECT"
GET_MSG = "!GET"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    # Finds the size of the message to send in the header
    message = msg.encode('utf-8')
    message_length = len(message)

    send_length = str(message_length).encode('utf-8')
    # Pads the header to be 8 bytes
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

send(GET_MSG)

msg_length = client.recv(HEADER).decode('utf-8')
if msg_length:
    msg_length = int(msg_length)

    raw_data = client.recv(msg_length)

send(DISCONNECT_MSG)

data = json.loads(raw_data)
print(round(float(data['temp']), 2))
