import paho.mqtt.client as paho
from paho.mqtt import client as mqtt_client

from utils import email_handler, rfid, buzzer
from datetime import datetime

client = paho.Client("client-007")
# broker = 'broker.emqx.io'
broker = 'localhost'
port = 1883
topics = [("Dashboard/RFID/Tag",0),("Dashboard/Light/Photo",1)]
# generate client ID with pub prefix randomly
client_id = 'Client456'
# username = 'emqx'
# password = 'public'

running = False

scanned_tag = -1
light_intensity = 0

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        content = msg.payload.decode()
        if msg.topic == "Dashboard/RFID/Tag":
            global scanned_tag
            scanned_tag = content
            print(f"Scanned Tag: {scanned_tag}")
            
            #check if tag is allowed
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if rfid.is_tag_authorized(scanned_tag):
                email_handler.send_email(f"Dashboard Authorized Login - (Tag:{scanned_tag})", f"At {current_time}, {rfid.get_name_of_tag(scanned_tag)} is here.")
            else:
                email_handler.send_email(f"Unauthorized Login Attempt - (Tag:{scanned_tag})", f"At {current_time}, unauthorized user tried accessing the dashboard.")
                buzzer.sound_buzzer()
                
        elif msg.topic == "Dashboard/Light/Photo":
            global light_intensity
            light_intensity = content
            #print(f"Received Light Intensity: {light_intensity}")

    client.subscribe(topics)
    client.on_message = on_message

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            subscribe(client)
#             subscribe(client, "Dashboard/Light/Photo")
            #print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run():
    global running
    if not running:
        running = True
        client = connect_mqtt()
        client.loop_start()
    
if __name__ == 'utils.mqtt_server' or __name__ == "__main__":
    run()