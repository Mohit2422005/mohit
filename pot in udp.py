import time
time.sleep(1)
import network
import socket

from machine import ADC, Pin

from gpio_lcd import GpioLcd
import time
lcd=GpioLcd(rs_pin=Pin(8),enable_pin=Pin(9),d4_pin=Pin(10),d5_pin=Pin(11),d6_pin=Pin(12),d7_pin=Pin(13))



pot = ADC(Pin(28))  

# Configure WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("POCO M6 Pro 5G", "mohit123")

# Remote port
UDP_PORT = 1234

# Wait for WiFi connection
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('WiFi connection failed')
else:
    print('Connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)

# Local IP and port
localIP = wlan.ifconfig()[0]
localPort = 1234
bufferSize = 1024

# Create a UDP socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and port
UDPServerSocket.bind((localIP, localPort))
print('Waiting for UDP packets...')

# Variable to store the last connected client's address
last_client_address = None

while True:
    if last_client_address is None:
        # Wait for a client to connect
        print("Waiting for a client...")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        last_client_address = bytesAddressPair[1]
        print(f"Connected to client: {last_client_address}")

    # Read ADC value
    adc_value = pot.read_u16()
    print(adc_value)

    # Send ADC value to the last connected client
    response_message = f"ADC Value: {adc_value}"
    UDPServerSocket.sendto(response_message.encode(), last_client_address)

    # Debugging prints
    print(f"Sent: {response_message} to {last_client_address}")

    # Delay for repeated sending (adjust as needed)
    time.sleep(.5)
    
    
    lcd.move_to(0,0)
    lcd.putstr(str(response_message                 ))
