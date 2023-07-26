import socket
import weatherhat
import json
import time

SERVER = "192.168.68.114"
PORT = 1337 
HEADER = 8  
DISCONNECT_MSG = "!DISCONNECT"
PUT_MSG = "!PUT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

sensor = weatherhat.WeatherHAT()
sensor.update(interval=1.0) # Update interval for wind and rain sensors

def send(msg):
    # Finds the size of the message to send in the header
    message = msg.encode('utf-8')
    message_length = len(message)

    # Makes the header and pads it to be 8 bytes
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

weather_data = {
"temp": sensor.device_temperature,
"humidity": sensor.humidity,
"dewPoint":  sensor.dewpoint,
"light": sensor.lux,
"pressure": sensor.pressure,
"windSpeed": sensor.wind_speed,
"windDirection": sensor.wind_direction,
"rain": sensor.rain,
"time": time.strftime('%l:%M%p %Z on %b %d, %Y')
}

send(PUT_MSG)
send(json.dumps(weather_data))
send(DISCONNECT_MSG)
