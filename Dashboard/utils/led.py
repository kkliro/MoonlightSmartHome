# import RPi.GPIO as GPIO

# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM)
LEDs = [17, 26]

led_light_states = LEDs

# initialize states to 0
for i, s in enumerate(led_light_states):
	led_light_states[i] = 0

# for LED in LEDs:
#     GPIO.setup(LED, GPIO.OUT)


# def set_led_output(output, light):
	# GPIO.output(light, output)