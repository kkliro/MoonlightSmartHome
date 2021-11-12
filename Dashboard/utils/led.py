import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LEDs = [17]

for LED in LEDs:
    GPIO.setup(LED, GPIO.OUT)


def set_led_output(output):
    for LED in LEDs:
        GPIO.output(LED, output)