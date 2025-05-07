#ifndef HADiscoveryConfig_h
#define HADiscoveryConfig_h

#include <ArduinoJson.h>
#include <MQTTTopicManager.h>

class HADiscoveryConfig {
public:
    HADiscoveryConfig(MQTTTopicManager& topicManager) : topics(topicManager) {}

    // Envoie la configuration pour un capteur
    void sendSensorConfig(const String& location, const String& sensor, 
                         const String& deviceClass, const String& unit, 
                         const String& friendlyName) {
        DynamicJsonDocument doc(512);
        String uniqueId = "esp32_" + topics.getMacAddress() + "_" + sensor;
        
        doc["name"] = friendlyName;
        doc["device_class"] = deviceClass;
        doc["state_topic"] = topics.getTopic(location, sensor, "state");
        doc["unit_of_measurement"] = unit;
        doc["unique_id"] = uniqueId;

        sendConfig("sensor", location + "_" + sensor, doc);
    }

    // Envoie la configuration pour un interrupteur
    void sendSwitchConfig(const String& location, const String& switchName, 
                         const String& friendlyName) {
        DynamicJsonDocument doc(512);
        String uniqueId = "esp32_" + topics.getMacAddress() + "_" + switchName;
        
        doc["name"] = friendlyName;
        doc["command_topic"] = topics.getTopic(location, switchName, "set");
        doc["state_topic"] = topics.getTopic(location, switchName, "state");
        doc["unique_id"] = uniqueId;

        sendConfig("switch", switchName, doc);
    }

private:
    MQTTTopicManager& topics;

    void sendConfig(const String& deviceType, const String& entityName, JsonDocument& config) {
        String topic = "homeassistant/" + deviceType + "/" + entityName + "/config";
        String payload;
        serializeJson(config, payload);
        topics.getClient().publish(topic.c_str(), payload.c_str(), true);
    }
};

#endif