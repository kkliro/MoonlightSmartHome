import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

LED = 26

GPIO.setup(LED, GPIO.OUT)

def get_resistance():
    # retrieve resistance from nodemcu
    resistance = 50
    return resistance

def set_led_output(output):
    GPIO.output(LED, output)