import network
import socket
import time
from machine import ADC,Pin

from gpio_lcd import GpioLcd
import time
lcd=GpioLcd(rs_pin=Pin(8),enable_pin=Pin(9),d4_pin=Pin(10),d5_pin=Pin(11),d6_pin=Pin(12),d7_pin=Pin(13))



# WiFi setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("POCO M6 Pro 5G", "mohit123")

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

print('Connected to WiFi, ready to send user input...')

# Start sending messages after Wi-Fi connection
client_ip = "192.168.43.1"  # Replace with your UDP server IP

while True:
    # Take input from user
    user_input = input("Enter message to send: ")

    # Send the user input message to the client over UDP
    send_message = f"{user_input}\n"

    UDPServerSocket.sendto(send_message.encode(), (client_ip, UDP_PORT))
    print(f"Sent: {send_message.strip()}")

    time.sleep(1)  # Optional: Add a delay between sending messages
    
    
    lcd.move_to(0,0)
    lcd.putstr(str(user_input))
