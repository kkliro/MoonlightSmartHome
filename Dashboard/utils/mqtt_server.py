import paho.mqtt.client as paho
from paho.mqtt import client as mqtt_client

client = paho.Client("client-007")
# broker = 'broker.emqx.io'
broker = 'localhost'
port = 1883
topic = "Dashboard/RFID/Tag"
# generate client ID with pub prefix randomly
client_id = 'Client456'
# username = 'emqx'
# password = 'public'

scanned_tag = -1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global scanned_tag
        scanned_tag = msg.payload.decode()
        #print(scanned_tag)

    client.subscribe(topic)
    client.on_message = on_message

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            subscribe(client)
            #print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    client.loop_start()
    
if __name__ == 'utils.mqtt_server' or __name__ == "__main__":
    run()