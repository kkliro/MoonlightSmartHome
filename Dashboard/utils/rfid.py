from time import sleep

from utils import mqtt_server

import sqlite3

con = sqlite3.connect('user_profiles.db',check_same_thread=False)
cur = con.cursor()

def get_temp_threshold(rfid_tag):
    if rfid_tag == "None":
        return 0
    cur.execute(f'SELECT temperature_threshold FROM preference_dict WHERE tag="{rfid_tag}"')
    return cur.fetchone()[0]


def get_photoresistor_threshold(rfid_tag):
    if rfid_tag == "None":
            return 0
    cur.execute(
        f'SELECT photoresistor_threshold FROM preference_dict WHERE tag="{rfid_tag}"')
    return cur.fetchone()[0]


def set_temp_threshold(rfid_tag, threshold):
    cur.execute(
        f'UPDATE preference_dict SET temperature_threshold = {threshold} WHERE tag="{rfid_tag}"')
    con.commit()


def set_photoresistor_threshold(rfid_tag, threshold):
    print("in set", threshold)
    cur.execute(
        f'UPDATE preference_dict SET photoresistor_threshold = {threshold} WHERE tag="{rfid_tag}"')
    con.commit()


def get_auth_user():
      with open("current_rfid_tag.txt", "r+") as file:
        return file.read()


def set_auth_user(rfid_tag):
    with open("current_rfid_tag.txt", "w") as file:
        file.write(rfid_tag)
        file.close() 

def get_user_name(tag):
    cur.execute(f'SELECT name FROM preference_dict WHERE tag="{tag}"')
    return cur.fetchone()[0]

stored_tags = {
    
    0: {
        'tag_id':18847127109,
        'name':'Konstantin K.',
        'temperature_threshold':10.0,
        'led_threshold':900.0,
        'rssi_threshold':2.0
    },

    1: {
        'tag_id':17253126109,
        'name':'Earvin-Carl D.',
        'temperature_threshold':29.0,
        'led_threshold':60.0,
        'rssi_threshold':4.0
    },
    
    2: {
        'tag_id':2432424213,
        'name':'Andrea T.',
        'temperature_threshold':25.0,
        'led_threshold':70.0,
        'rssi_threshold':3.0
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
    
def get_stored_tag_index(tag):
    tag = int(tag)
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == tag:
            return i

    return -1

def get_name_of_tag(tag):
    if is_tag_authorized(tag):
        return stored_tags[get_stored_tag_index(tag)]['name']
        
def set_led_threshold(value):
    if is_authorized():
        global stored_tags
        stored_tags[get_tag_in_store()]['led_threshold'] = value

def is_tag_authorized(tag):
    tag = int(tag)
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == tag:
            return True
        
    return False

def check_for_scanned_tag():
    global active_tag
    tag = int(mqtt_server.scanned_tag)
    if tag != active_tag:
        active_tag = tag
        print("Active tag changed to " + str(active_tag))
        
def set_tag(tag):
    global active_tag
    active_tag = tag
    
def get_rssi_threshold():
    if is_authorized():
        return stored_tags[get_tag_in_store()]['rssi_threshold']

def set_rssi_threshold(value):
    if is_authorized():
        global stored_tags
        stored_tags[get_tag_in_store()]['rssi_threshold'] = value