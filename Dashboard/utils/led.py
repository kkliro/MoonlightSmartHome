import RPi.GPIO as GPIO

from utils import mqtt_server

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LEDs = [17, 26] # LED GPIOs

led_light_states = LEDs.copy() # State of each LED

# Initialize states to 0
for i, s in enumerate(led_light_states):
    led_light_states[i] = False

for LED in LEDs:
    GPIO.setup(LED, GPIO.OUT)

# Get current light resistance
def get_resistance():
    # Retrieve resistance from nodemcu
    resistance = int(mqtt_server.light_intensity)
    return resistance
 
# Set LED output
def set_led_output(light, output):
    target = LEDs[light]
    GPIO.output(target, output)
 
# Get the state of an LED
def get_led_state(index):
    return led_light_states[index]

# Set state of LED
def set_led_state(index, value):
    global led_light_statess
    led_light_states[index] = value
    set_led_output(index, value)
    
set_led_state(0, False)
set_led_state(1, False)