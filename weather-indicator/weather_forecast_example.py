from VirtualCopernicusNG import TkCircuit
from pyowm.owm import OWM

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)


@circuit.run
def main():
    from time import sleep
    from gpiozero import AngularServo, Button

    owm = OWM('api_key')
    reg = owm.city_id_registry()
    mgr = owm.weather_manager()

    krakow = reg.ids_for('Kraków', country='PL')[0]
    istanbul = reg.ids_for('Istanbul', country='TR')[0]
    stockholm = reg.ids_for('Stockholm', country='SE')[0]

    global btn_state
    btn_state = 0

    CITIES = [krakow, istanbul, stockholm]
    CITY_COUNT = 3
    WEATHER = {
        'clear': -70,
        'mist': -30,
        'haze': -30,
        'smoke': 10,
        'dust': 10,
        'sand': 10,
        'clouds': 10,
        'ash': 10,
        'squall': 10,
        'drizzle': 50,
        'rain': 50,
        'snow': 50,
        'thunderstorm': 50,
        'tornado': 50

    }
    servo1 = AngularServo(17, min_angle=-90, max_angle=90)
    servo1.angle = -90

    def button1_pressed():
        global btn_state
        btn_state += 1
        print("Change to " + str(CITIES[btn_state % CITY_COUNT]))

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    while True:
        weather = mgr.weather_at_id(CITIES[btn_state % CITY_COUNT][0]).weather
        status = str(weather.status).lower()
        servo1.angle = WEATHER.get(status)
        print(str(CITIES[btn_state % CITY_COUNT]) + " : " + status)
        sleep(3)
