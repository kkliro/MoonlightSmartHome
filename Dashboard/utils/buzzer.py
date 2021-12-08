import RPi.GPIO as GPIO

import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
BUZZER = 20 #GPIO for buzzer

GPIO.setup(BUZZER, GPIO.OUT)

# Sounds the buzzer for 1 second when invoked
def sound_buzzer():
    GPIO.output(BUZZER, True)
    time.sleep(1)
    GPIO.output(BUZZER, False)
