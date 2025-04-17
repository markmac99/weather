/*
 * Wemos battery shield, measure Vbat
 * add 100k between Vbat and ADC
 * Voltage divider of 100k+220k over 100k
 * gives 100/420k
 * ergo 4.2V -> 1Volt on the pin
 * Max input on A0=1Volt -> count of 1023 
 * 4.2*(Raw/1023)=Vbat

 * adjust the resistor as needed
 */

// Connect RST to gpio16 (RST and D0 on Wemos)
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "secrets.h"

unsigned int raw = 0;
float volt = 0.0;
const int SLEEPSECS = 60;

WiFiClient espClient;
PubSubClient mqtt_client(espClient);

const char clientid[] = "test";

const char mqtt_topic[]  = "sensors/batteries/test/voltage";
const char mqtt_topic2[]  = "sensors/batteries/test/reading";


const int publish = 1; // set to zero to disable mq publ while testing 

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}

void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        Serial.printf("Connecting to MQTT Broker as %s.....\n", clientid);
        if (mqtt_client.connect(clientid, mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            // Publish message upon successful connection
            // mqtt_client.publish(mqtt_topic, "Hi I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    mqtt_client.setServer(mqtt_broker, mqtt_port);
    connectToMQTTBroker();
}

void loop() {
  raw = analogRead(A0);
  volt=raw/1023.0;
  volt=volt*4.2;

  if (publish)
  {
    String payload=String(volt);

    connectToMQTTBroker();

    if (mqtt_client.publish(mqtt_topic, payload.c_str(), true))
        Serial.println("Message published ["+String(mqtt_topic)+"]: "+payload);
    else
      Serial.println("Problem publishing ["+String(mqtt_topic)+"]: "+payload);

    payload=String(raw);
    if (mqtt_client.publish(mqtt_topic2, payload.c_str(), true))
        Serial.println("Message published ["+String(mqtt_topic2)+"]: "+payload);
    else
      Serial.println("Problem publishing ["+String(mqtt_topic2)+"]: "+payload);
  }
  else
  {
      Serial.println("simulated publish");
  }
  Serial.println("sleeping...");
  delay(SLEEPSECS*1000);
}