import RPi.GPIO as GPIO

from utils import mqtt_server

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LEDs = [17, 26]

led_light_states = LEDs.copy()

# initialize states to 0
for i, s in enumerate(led_light_states):
    led_light_states[i] = False

for LED in LEDs:
    GPIO.setup(LED, GPIO.OUT)

def get_resistance():
    # retrieve resistance from nodemcu
    resistance = int(mqtt_server.light_intensity)
    return resistance

def set_led_output(light, output):
    target = LEDs[light]
    GPIO.output(target, output)

def get_led_state(index):
    global led_light_states
    return led_light_states[index]

def set_led_state(index, value):
    global led_light_statess
    led_light_states[index] = value
    set_led_output(index, value)