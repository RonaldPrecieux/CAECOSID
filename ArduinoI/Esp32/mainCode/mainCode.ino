#include <WiFi.h>
#include <PubSubClient.h>
#include "MQTTDevice.h"

class MySmartHomeDevice : public MQTTDevice {
public:
    // Utilisation de WiFi.macAddress() pour ESP32
    MySmartHomeDevice() : MQTTDevice(getMacAddress()) {}

    String getMacAddress() {
        uint8_t mac[6];
        WiFi.macAddress(mac);
        char macStr[18] = {0};
        snprintf(macStr, sizeof(macStr), "%02X%02X%02X%02X%02X%02X", 
                 mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
        return String(macStr);
    }

    void setupHA() {
        // Envoyer les configurations avec gestion des erreurs
        if(!getHAConfig().sendSensorConfig("cuisine", "temperature", "temperature", "°C", "Température Salon")) {
            Serial.println("Échec de la configuration du capteur de température");
        }
        Serial.println("Succès de la configuration du capteur de température");
        
        delay(500); // Délai entre les configurations
        
        if(!getHAConfig().sendSensorConfig("cuisine", "humidite", "humidity", "%", "Humidité Cuisine")) {
            Serial.println("Échec de la configuration du capteur d'humidité");
        }
        Serial.println("Succès de la configuration du capteur d'humidité");
        
        delay(500);
        
        if(!getHAConfig().sendSwitchConfig("cuisine", "lampe", "Lampe Cuisine")) {
            Serial.println("Échec de la configuration de la lampe");
        }
        Serial.println("Succès de la configuration de la lampe");
    }

    void handleCommand(const String& location, const String& device, const String& value) override {
        if (device == "lampe") {
            // Contrôler la lampe
            Serial.print("Commande lampe reçue: ");
            Serial.println(value);
            publishSensorData(location, device, value); // Mettre à jour l'état
            Serial.printf("Commande Lampe reçue et exécutée %s dans la %s\n", value.c_str(), location.c_str());
        }
        // ... autres commandes
    }
};

MySmartHomeDevice device;

void setup() {
    Serial.begin(115200);
    
    // Utilisation de begin() au lieu de setup()
    device.begin("TP-LINK_8D4A", "79791625", "192.168.0.106");
    
    // Attendre que la connexion soit stable
    delay(2000);
    
    // Configuration des appareils Home Assistant
    device.setupHA();
}

void loop() {
    // Utilisation de handle() au lieu de loop()
    device.handle();
    
    // Simuler des données de capteurs
    static unsigned long lastSend = 0;
    if (millis() - lastSend > 5000) {
        float temp = random(200, 300) / 10.0;
        device.publishSensorData("cuisine", "temperature", temp);
        
        float hum = random(300, 800) / 10.0;
        device.publishSensorData("cuisine", "humidite", hum);
        
        lastSend = millis();
    }
}