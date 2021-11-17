from time import sleep

stored_tags = {
    
    0: {
        'tag_id':123,
        'name':'Bob Joe',
        'temperature_threshold':25.0,
        'led_threshold':10.0
    },

    1: {
        'tag_id':456,
        'name':'Random Name',
        'temperature_threshold':5.0,
        'led_threshold':20.0
    }

}

# active_tag = len(stored_tags)
active_tag = 456

def is_authorized():
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == active_tag:
            return True

    return False

def get_tag_in_store():
    for i in range(len(stored_tags)):
        current_tag = stored_tags[i]
        if current_tag['tag_id'] == active_tag:
            return i

    return -1

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

def set_tag(tag):
    global active_tag
    active_tag = tag