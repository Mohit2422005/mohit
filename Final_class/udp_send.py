import network
import socket
import time
import machine

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("hiii","0987654321")

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    print("Connecting...")
    time.sleep(1)
    max_wait -= 1

# Check connection
if not wlan.isconnected():
    print("Connection failed!")
else:
    ip = wlan.ifconfig()[0]
    print("Connected! IP:", ip)

# Setup LED pin (e.g., onboard LED on GP2 or built-in LED on Pico W = "LED")
led = machine.Pin("LED", machine.Pin.OUT)
led1=machine.Pin(2,machine.Pin.OUT)
led2=machine.Pin(3,machine.Pin.OUT)
buz=machine.Pin(6,machine.Pin.OUT)
rel=machine.Pin(7,machine.Pin.OUT)
# Setup UDP
localIP = ip
localPort = 1234
bufferSize = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((localIP, localPort))
print("UDP Server listening at:", localIP, "port:", localPort)

# Main loop
while True:
    data, addr = sock.recvfrom(bufferSize)
    msg = data.decode().strip()
    print("Received:", msg, "from", addr)

    if msg == "1":
        led.on()
        print("LED ON")
    elif msg == "2":
        led.off()
    elif msg == "3":
        led1.on()
    elif msg == "4":
        led1.off()
    elif msg == "5":
        led2.on()
    elif msg == "6":
        led2.off()
    elif msg == "7":
        buz.on()
    elif msg == "8":
        buz.off()   
    elif msg == "9":
        rel.on()
    elif msg == "10":
        rel.off()  
        
    else:
        print("Unknown command")

