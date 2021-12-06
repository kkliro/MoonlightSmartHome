from time import sleep

from utils import mqtt_server

import sqlite3
import threading

con = sqlite3.connect('user_profiles.db',check_same_thread=False)
cur = con.cursor()

lock = threading.Lock()

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

def check_if_exists(tag):
    try:
        lock.acquire(True)
        cur.execute(f'SELECT EXISTS(SELECT user_id FROM user_preferences WHERE user_id="{tag}")')
        return cur.fetchone()[0]
    finally:
        lock.release()

def is_authorized():
    if check_if_exists(active_tag) == 1:
        return True
    return False
#     global active_tag
#     for i in range(len(stored_tags)):
#         current_tag = stored_tags[i]
#         if current_tag['tag_id'] == active_tag:
#             return True
#         
#     return False

def get_temperature_threshold():
    if is_authorized():
#         return stored_tags[get_tag_in_store()]['temperature_threshold']
        try:
            lock.acquire(True)
            cur.execute(f'SELECT temp_threshold FROM user_preferences WHERE user_id="{active_tag}"')
            return cur.fetchone()[0]
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
            #print(error.args[0])
        finally:
            lock.release()
        

def set_temperature_threshold(value):
    if is_authorized():
#         global stored_tags
#         stored_tags[get_tag_in_store()]['temperature_threshold'] = value
        try:
            lock.acquire(True)
            cur.execute(f'UPDATE user_preferences SET temp_threshold = {value} WHERE user_id="{active_tag}"')
            con.commit()
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
            #print(error.args[0])
        finally:
            lock.release()

def get_led_threshold():
    if is_authorized():
#         return stored_tags[get_tag_in_store()]['led_threshold']
        try:
            lock.acquire(True)
            cur.execute(f'SELECT light_threshold FROM user_preferences WHERE user_id="{active_tag}"')
            return cur.fetchone()[0]
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
            #print(error.args[0])
        finally:
            lock.release()

def get_profile_name():
    if is_authorized():
        try:
            lock.acquire(True)
            cur.execute(f'SELECT name FROM user_preferences WHERE user_id="{active_tag}"')
            return cur.fetchone()[0]
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
            #print(error.args[0])
        finally:
            lock.release()
        #return stored_tags[get_tag_in_store()]['name']
    
# def get_stored_tag_index(tag):
#     tag = int(tag)
#     for i in range(len(stored_tags)):
#         current_tag = stored_tags[i]
#         if current_tag['tag_id'] == tag:
#             return i
# 
#     return -1

def get_name_of_tag(tag):
    if is_tag_authorized(tag):
        try:
            lock.acquire(True)
            cur.execute(f'SELECT name FROM user_preferences WHERE user_id="{tag}"')
            return cur.fetchone()[0]
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
        finally:
            lock.release()
            #print(error.args[0])
        #return stored_tags[get_tag_in_store()]['name']
        #return stored_tags[get_stored_tag_index(tag)]['name']
        
def set_led_threshold(value):
    if is_authorized():
#         global stored_tags
#         stored_tags[get_tag_in_store()]['led_threshold'] = value
        try:
            lock.acquire(True)
            cur.execute(f'UPDATE user_preferences SET light_threshold = {value} WHERE user_id="{active_tag}"')
            con.commit()
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
            #print(error.args[0])
        finally:
            lock.release()

def is_tag_authorized(tag):
    tag = int(tag)
    if check_if_exists(tag) == 1:
        return True
    return False
#     for i in range(len(stored_tags)):
#         current_tag = stored_tags[i]
#         if current_tag['tag_id'] == tag:
#             return True
#         
#     return False

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
        try:
            lock.acquire(True)
            cur.execute(f'SELECT rssi_threshold FROM user_preferences WHERE user_id="{active_tag}"')
            return cur.fetchone()[0]
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
        finally:
            lock.release()
#         return stored_tags[get_tag_in_store()]['rssi_threshold']

def set_rssi_threshold(value):
    if is_authorized():
        try:
            lock.acquire(True)
            cur.execute(f'UPDATE user_preferences SET rssi_threshold = {value} WHERE user_id="{active_tag}"')
            con.commit()
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("No data found")
        finally:
            lock.release()
#         global stored_tags
#         stored_tags[get_tag_in_store()]['rssi_threshold'] = value