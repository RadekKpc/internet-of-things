from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "living_room",
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
        mqttc.publish("zone1/light", "off", 0, False)

    def switch_1_pressed():
        print("SW1 presed!")
        led1.toggle()

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
        mqttc.subscribe("livingroom/light/lamp1")
        mqttc.subscribe("zone2/light")
        mqttc.subscribe("zone1/light")
        mqttc.subscribe("livingroom/service")
        mqttc.publish("livingroom/service", "Light controller living_room is working properly", 0, False)
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

        if str(msg.payload) == "b'off'" and "light" in msg.topic:
            led1.off()


    # If you want to use a specific client id, use
    # mqttc = mqtt.Client("client-id")
    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    mqttc = mqtt.Client("kopec-radek-livingroom-1")
    mqttc.will_set("livingroom/service", "Light controller livingroom is not working", False, 0)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()
