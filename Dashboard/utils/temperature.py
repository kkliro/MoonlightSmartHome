# import RPi.GPIO as GPIO

# import time
# import board
# import adafruit_dht

# dhtDevice = adafruit_dht.DHT11(board.D4)

temperature_threshold = 25.0

_temperature = [0,0]
_humidity = [0,0]

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

def set_temperature_threshold(value):
    global temperature_threshold
    temperature_threshold = value

def set_humidity(new_humidity):
    global _humidity
    _humidity[1] = _humidity[0]
    _humidity[0] = new_humidity

def set_temperature(new_temperature):
    global _temperature
    _temperature[1] = _temperature[0]
    _temperature[0] = new_temperature