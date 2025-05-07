
#ifndef MQTTTopicManager_h
#define MQTTTopicManager_h

#include <Arduino.h>
#include <PubSubClient.h>

class MQTTTopicManager {
public:
    MQTTTopicManager(PubSubClient& mqttClient, const String& deviceMac)
        : client(mqttClient), macAddress(deviceMac) {}

    // Génère les topics de base
    String getBaseTopic(const String& location = "") {
        if (location.isEmpty()) {
            return "home/esp32-" + macAddress;
        }
        return "home/" + location + "/esp32-" + macAddress;
    }

    // Génère un topic complet pour un capteur/actionneur
    String getTopic(const String& location, const String& device, const String& type) {
        return getBaseTopic(location) + "/" + device + "/" + type;
    }

    // Publie un message avec le topic construit automatiquement
    bool publish(const String& location, const String& device, const String& type, const String& payload, bool retained = false) {
        String topic = getTopic(location, device, type);
        return client.publish(topic.c_str(), payload.c_str(), retained);
    }

private:
    PubSubClient& client;
    String macAddress;
};

#endif
