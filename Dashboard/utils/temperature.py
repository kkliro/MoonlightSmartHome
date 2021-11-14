# import RPi.GPIO as GPIO

# import time
# import board
# import adafruit_dht

# dhtDevice = adafruit_dht.DHT11(board.D4)

def get_temp():
    try:
        return 11
        # return dhtDevice.temperature
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        
def get_humidity():
    try:
        return 50
        # return dhtDevice.humidity
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])