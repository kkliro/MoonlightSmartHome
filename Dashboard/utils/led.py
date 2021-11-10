import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LED = 23
GPIO.setup(LED, GPIO.OUT)

def setLEDOutput(output):
    GPIO.output(LED, output)  