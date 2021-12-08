import RPi.GPIO as GPIO

import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4)

_temperature = [0,0]
_humidity = [0,0]

# Get current temperature reading
def get_temp():
    try:
        return dhtDevice.temperature
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        
# Get current humidity reading
def get_humidity():
    try:
        return dhtDevice.humidity
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

# Set humidity records
def set_humidity(new_humidity):
    global _humidity
    _humidity[1] = _humidity[0]
    _humidity[0] = new_humidity

# Set temperature records
def set_temperature(new_temperature):
    global _temperature
    _temperature[1] = _temperature[0]
    _temperature[0] = new_temperature