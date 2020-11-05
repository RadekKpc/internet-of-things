from VirtualCopernicusNG import TkCircuit

# set up sockets at the udp
import socket
import struct

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# initialize the circuit inside the

configuration = {
    "name": "Bedroom",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ],
    "buzzers": [
        {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
    ]
}

circuit = TkCircuit(configuration)

@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    from time import sleep

    from CustomProtocol import CustomProtocol

    def on_change(device):
        if device == "lamp1":
            led1.toggle()
        if device == "lamp2":
            led2.toggle()

    def on_on(device):
        if device == "lamp1":
            led1.on()
        if device == "lamp2":
            led2.on()

    def on_off(device):
        if device == "lamp1":
            led1.off()
        if device == "lamp2":
            led2.off()

    protocol = CustomProtocol("f1", "bathroom", "1", ["lamp1", "lamp2"], on_change, on_off, on_on)


    def switch_2_pressed():
        print("Lamp 2 toggle!")
        led2.toggle()

    def switch_1_pressed():
        print("Lamp 1 toggle!")
        led1.toggle()

    led2 = LED(22)
    led1 = LED(21)

    button1 = Button(11)
    button1.when_pressed = switch_1_pressed

    button2 = Button(12)
    button2.when_pressed = switch_2_pressed

    while True:
        command = sock.recv(10240)
        command = command.decode("utf-8")
        print(command.split(';'))
        command = command.split(';')
        if protocol.match(command):
            print("command match")
            protocol.execute(command)
        sleep(0.1)

        sleep(0.1)