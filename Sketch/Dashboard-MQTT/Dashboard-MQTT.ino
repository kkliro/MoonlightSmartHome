#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const char* ssid = "TP-Link_8856";
const char* password = "87973365";

const char* mqtt_server = "192.168.0.101"; // Pi I

WiFiClient vanieriot;
PubSubClient client(vanieriot);

#include <SPI.h>
#include <MFRC522.h>
#define D3 0
#define D4 2
constexpr uint8_t RST_PIN = D3;     // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D4;     // Configurable, see typical pin layout above
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
String tag;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }

  if (topic == "RFID/Tag") {
      Serial.println("Light is ON");
  }

}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");


    //  String clientId = "ESP8266Client-";
    // clientId += String(random(0xffff), HEX);
    // Attempt to connect
    // if (client.connect(clientId.c_str())) {
    if (client.connect("vanieriot")) {

      Serial.println("connected");
      client.subscribe("room/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {

  Serial.begin(115200);
  setup_wifi();
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  if (!client.loop())
    client.connect("smarthome_dashboard_iotvanier");

  int sensorValue = analogRead(A0);
  String photoResistorVal = String(sensorValue);

  char cbuf[30];
  photoResistorVal.toCharArray(cbuf, photoResistorVal.length() + 1);
  client.publish("Dashboard/Light/Photo", cbuf);
  //Serial.println(cbuf);

  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if (rfid.PICC_ReadCardSerial()) {
    for (byte i = 0; i < 4; i++) {
      tag += rfid.uid.uidByte[i];
    }
    char buf[30];
    tag.toCharArray(buf, tag.length() + 1);
    client.publish("Dashboard/RFID/Tag", buf);
    Serial.println(buf);
    tag = "";
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }



  //  char hh [8];
  //  dtostrf(h,6,2,hh);
  //  char tt [8];
  //  dtostrf(t,6,2,tt);

  //client.publish("IoTlab/ESP", "Hello IoTlab");
  
  //  client.publish("device/alh",hh);

  delay(1000);
}
