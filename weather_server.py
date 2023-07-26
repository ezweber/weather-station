import socket
import threading
import csv
import json

HOST = ""  # Empty string will listen on all interfaces
PORT = 1337
HEADER = 8 
DISCONNECT_MSG = "!DISCONNECT"
GET_MSG = "!GET"
PUT_MSG = "!PUT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    while True:
        # Gets a fixed size header that will hold the size of the next message
        msg_length = conn.recv(HEADER).decode('utf-8')

        if msg_length: # Checks if the message is isn't null
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')

            if msg == DISCONNECT_MSG:
                print(f"Client {addr[0]} disconnected. ")
                break

            if msg == GET_MSG:
                send_data(conn)

            if msg == PUT_MSG:
                receive_data(conn)

            print(f"{addr} sent {msg}")

    conn.close()

def receive_data(conn):
    msg_length = conn.recv(HEADER).decode('utf-8')
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode('utf-8')
        
        weather_data = json.loads(msg)
        with open('weather_data.csv','a') as f:
            w = csv.writer(f)
            w.writerows(weather_data.items())

def send_data(conn):
    # Read the last 9 lines from the weather data file using CSV module
    with open('weather_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)[-9:]

    # Convert the lines into a dictionary
    data_dict = {}
    for line in lines:
        key, *values = line
        data_dict[key] = values[0]

    # Send the data dictionary as JSON and the size header over the connection
    message = json.dumps(data_dict).encode('utf-8')
    message_length = len(message)

    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        # Handle the connection in its own thread so we can go back to listening and handle multiple clients at a time
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.activeCount() - 1} active connections.")

print("Starting server")
print(f"Listening on port {PORT}")
start()
