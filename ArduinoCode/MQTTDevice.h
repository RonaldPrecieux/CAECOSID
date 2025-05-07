#ifndef MQTTDevice_h
#define MQTTDevice_h

#include <WiFi.h>
#include <PubSubClient.h>
#include "MQTTTopicManager.h"
#include "HADiscoveryConfig.h"

class MQTTDevice {
public:
    MQTTDevice(const String& macAddress)
        : wifiClient(), 
          mqttClient(wifiClient), 
          topicManager(mqttClient, macAddress),
          haConfig(topicManager) {}

    void setup(const char* ssid, const char* password, const char* mqttServer, int mqttPort = 1883) {
        connectWiFi(ssid, password);
        mqttClient.setServer(mqttServer, mqttPort);
        mqttClient.setCallback([this](char* topic, byte* payload, unsigned int length) {
            this->mqttCallback(topic, payload, length);
        });
    }

    void loop() {
        if (!mqttClient.connected()) {
            reconnect();
        }
        mqttClient.loop();
    }

    // Méthodes pour publier des données
    void publishSensorData(const String& location, const String& sensor, const String& value) {
        topicManager.publish(location, sensor, "state", value, true);
    }

    // Méthodes pour gérer les commandes (à implémenter dans la classe dérivée)
    virtual void handleCommand(const String& location, const String& device, const String& value) = 0;

    // Gestion de la configuration Home Assistant
    HADiscoveryConfig& getHAConfig() { return haConfig; }

protected:
    WiFiClient wifiClient;
    PubSubClient mqttClient;
    MQTTTopicManager topicManager;
    HADiscoveryConfig haConfig;

private:
    void connectWiFi(const char* ssid, const char* password) {
        WiFi.begin(ssid, password);
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
        }
    }

    void reconnect() {
        while (!mqttClient.connected()) {
            if (mqttClient.connect("ESP32Client")) {
                // S'abonner aux topics nécessaires
                mqttClient.subscribe(topicManager.getTopic("", "+", "set").c_str());
                mqttClient.subscribe(topicManager.getTopic("salon", "+", "set").c_str());
                // ... autres abonnements
            } else {
                delay(5000);
            }
        }
    }

    void mqttCallback(char* topic, byte* payload, unsigned int length) {
        String topicStr = String(topic);
        String payloadStr;
        for (unsigned int i = 0; i < length; i++) {
            payloadStr += (char)payload[i];
        }

        // Extraire location et device du topic
        // Format: home/[location]/esp32-MAC/device/set
        int locStart = topicStr.indexOf("home/") + 5;
        int locEnd = topicStr.indexOf('/', locStart);
        String location = topicStr.substring(locStart, locEnd);
        
        int devStart = locEnd + 1;
        int devEnd = topicStr.indexOf('/', devStart);
        String device = topicStr.substring(devStart, devEnd);

        handleCommand(location, device, payloadStr);
    }
};

#endif