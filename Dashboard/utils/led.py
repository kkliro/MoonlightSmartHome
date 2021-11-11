import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LED = 17
GPIO.setup(LED, GPIO.OUT)

def set_led_output(output):
    GPIO.output(LED, output)