from time import sleep

from utils import mqtt_server

import sqlite3
import threading

con = sqlite3.connect('user_profiles.db',check_same_thread=False)
cur = con.cursor()

lock = threading.Lock()

active_tag = -1

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

def get_temperature_threshold():
    if is_authorized():
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
        
def set_led_threshold(value):
    if is_authorized():
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