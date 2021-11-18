from time import sleep
from datetime import datetime

from utils import mqtt_server, email_handler

stored_tags = {
    
    0: {
        'tag_id':18847127109,
        'name':'Konstantin K.',
        'temperature_threshold':10.0,
        'led_threshold':900.0
    },

    1: {
        'tag_id':1725312610,
        'name':'Earvin-Carl D.',
        'temperature_threshold':5.0,
        'led_threshold':60.0
    },
    
    2: {
        'tag_id':2432424213,
        'name':'Andrea T.',
        'temperature_threshold':25.0,
        'led_threshold':70.0
    }

}

# active_tag = len(stored_tags)
active_tag = -1

def get_tag_in_store():
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == active_tag:
            return i

    return -1

def is_authorized():
    global active_tag
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == active_tag:
            return True
        
    return False

def get_temperature_threshold():
    if is_authorized():
        return stored_tags[get_tag_in_store()]['temperature_threshold']

def set_temperature_threshold(value):
    if is_authorized():
        global stored_tags
        stored_tags[get_tag_in_store()]['temperature_threshold'] = value

def get_led_threshold():
    if is_authorized():
        return stored_tags[get_tag_in_store()]['led_threshold']

def get_profile_name():
    if is_authorized():
        return stored_tags[get_tag_in_store()]['name'] 

def set_led_threshold(value):
    if is_authorized():
        global stored_tags
        stored_tags[get_tag_in_store()]['led_threshold'] = value

def check_for_scanned_tag():
    global active_tag
    tag = int(mqtt_server.scanned_tag)
    if tag != active_tag:
        active_tag = tag
        print("Active tag changed to " + str(active_tag))
        if is_authorized():
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            email_handler.send_email(f"Dashboard Authorized Login - (Tag - {active_tag})", f"At {current_time}, {get_profile_name()} is here.")
        
def set_tag(tag):
    global active_tag
    active_tag = tag