import os
import re
import json
from datetime import datetime

last_checked_time = None

def scan_devices():
    global last_checked_time
    
    print("Scanning...")
    
    device_details = {}
    device_count = 0
    
    bashCommand = "sudo node /home/pi/SmartHome/Dashboard/utils/get_devices.js >| output.txt"
    devices = os.system(bashCommand)
    device_list = []
    rssi_list = []
    information_dict = {}
    with open('output.txt',encoding='utf-8-sig', errors='ignore') as devices:
        sp = devices.read().splitlines()

    for line in sp:
        rssi = 0;
        transmitterId = "";
        if "transmitterId:" in line:
            transmitter_id = line.split("'")[1::2]
            device_list.append(transmitter_id)
        if "rssi:" in line:
            rssi = int(re.search(r'\d+', line).group(0))
            rssi_list.append(rssi)
    
    for i in range(len(device_list)):
        information_dict[device_list[i][0]] = rssi_list[i]

    device_count = len(information_dict)
    
    info = {'device_count':device_count, 'details':information_dict}
    
    now = datetime.now()
    
    last_checked_time = now.strftime("%H:%M:%S")
        
    return(info)
    
def get_last_checked_time():
    global last_checked_time
    return last_checked_time