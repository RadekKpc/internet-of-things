from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "bedroom",
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
    ]
}

circuit = TkCircuit(configuration)


# mqttc.publish("temp/floor1/room1/pref1", "20", 0, False)
@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import paho.mqtt.client as mqtt

    def switch_2_pressed():
        print("SW2 presed!")
        led2.toggle()

    def switch_1_pressed():
        print("SW1 presed!")
        led1.toggle()

    led2 = LED(22)
    led1 = LED(21)

    button1 = Button(11)
    button1.when_pressed = switch_1_pressed

    button2 = Button(12)
    button2.when_pressed = switch_2_pressed

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        mqttc.subscribe("bedroom/light/lamp1")
        mqttc.subscribe("bedroom/light/lamp2")
        mqttc.subscribe("zone2/light")
        mqttc.subscribe("bedroom/service")
        mqttc.publish("bedroom/service", "Light controller bedroom is working properly", 0, False)
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if str(msg.payload) == "b'off'" and "lamp1" in msg.topic:
            led1.off()
        if str(msg.payload) == "b'off'" and "lamp2" in msg.topic:
            led1.off()
        if str(msg.payload) == "b'off'" and "zone2/light" in msg.topic:
            led1.off()
            led2.off()
    # If you want to use a specific client id, use
    # mqttc = mqtt.Client("client-id")
    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    mqttc = mqtt.Client("kopec-radek-bedroom-1")
    mqttc.will_set("bedroom/service", "Light controller bedroom is not working", False, 0)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()