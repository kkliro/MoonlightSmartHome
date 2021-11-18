import RPi.GPIO as GPIO

GPIO.setwarnings(False)

input1 = 24
enable1 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(input1, GPIO.OUT)
GPIO.setup(enable1, GPIO.OUT)

pwm = GPIO.PWM(enable1, 100)
pwm.start(0)
          
GPIO.output(input1, 1)

GPIO.output(enable1, 1)

motor_state = False

def change_motor_state(state):
    global motor_state
    motor_state = state

    print(motor_state)
    
    if motor_state:
        pwm.ChangeDutyCycle(50)
    else:
        pwm.ChangeDutyCycle(0)
