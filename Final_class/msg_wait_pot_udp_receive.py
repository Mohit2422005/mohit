import network
import socket
import time
from machine import ADC

# WiFi setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("temp", "12345678")

pot = ADC(28)

UDP_PORT = 1234  # Port to send data

# Wait for connection
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('WiFi connection failed')
else:
    print('Connected')
    ip = wlan.ifconfig()[0]
    print('IP:', ip)

localIP = ip
localPort = 1234
bufferSize = 1024

# Create UDP socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print('UDP server waiting for start message...')

start_sending = False
client_ip = None

while True:
    if not start_sending:
        # Wait for first message
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        client_ip = address[0]

        print(f"Received start message: {message} from {address}")
        start_sending = True

    else:
        # Read ADC value
        adc_value = pot.read_u16()

        # Send ADC value with "ADC : " before each value
        send_message = f"ADC : {adc_value}\n"

        UDPServerSocket.sendto(send_message.encode(), (client_ip, UDP_PORT))
        print(f"Sent: {send_message.strip()}")

        time.sleep(1)
