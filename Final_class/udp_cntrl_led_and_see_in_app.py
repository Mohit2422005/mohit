import network
import socket
import time
from machine import Pin

led = Pin(2, Pin.OUT)

# WiFi Connect
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("hii", "1234567890")
 
# remote port
UDP_IP = "192.168.43.1"
UDP_PORT = 1234
 
# Wait for connect or fail
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)

# Create a UDP socket
localIP  = wlan.ifconfig()[0]
localPort = 1234
bufferSize = 1024

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print('waiting....')

while True:
    # receive
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode().strip().lower()
    address = bytesAddressPair[1]
    UDP_IP = address[0]

    print("Received from", UDP_IP, ":", message)

    # control LED
    if message == "on":
        led.value(1)
        reply_message = "LED is ON"
    elif message == "off":
        led.value(0)
        reply_message = "LED is OFF"
    else:
        reply_message = "Unknown Command"

    # send back reply
    UDPServerSocket.sendto(reply_message.encode(), (UDP_IP, UDP_PORT))
    
    time.sleep(2)
