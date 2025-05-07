#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "MQTTDevice.h"

class MySmartHomeDevice : public MQTTDevice {
public:
    // Utilisation de WiFi.macAddress() pour ESP8266
    MySmartHomeDevice() : MQTTDevice(WiFi.macAddress()) {}

    void setupHA() {
            
        // Envoyer les configurations avec gestion des erreurs
        getHAConfig().sendSensorConfig("cuisine", "temperature", "temperature", "°C", "Température Salon");
        Serial.println("Succes de la configuration du capteur de température");
        
        
        delay(500); // Délai entre les configurations
        
        getHAConfig().sendSensorConfig("cuisine", "humidite", "humidity", "%", "Humidité Cuisine");
        Serial.println("Succes de la configuration du capteur d'humidité");
        
        
        delay(500);
        
        getHAConfig().sendSwitchConfig("cuisine", "lampe", "Lampe Cuisine");
        Serial.println("Succes de la configuration de la lampe");
        
        getHAConfig().sendSwitchConfig("cuisine", "lampe", "Lampe Cuisine");
        Serial.println("Succes de la configuration de la lampe");
        
        
        // Configurer les capteurs

        //getHAConfig().sendSwitchConfig("salon", "prise_tele", "Prise Télé");
    }

    void handleCommand(const String& location, const String& device, const String& value) override {
        if (device == "lampe") {
            // Contrôler la lampe
            Serial.print("Commande lampe reçue: ");
            Serial.println(value);
            publishSensorData(location, device, value); // Mettre à jour l'état
            Serial.printf("Commande Lampe recu et exeuté %s dans la ",location);
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
    //device.setupHA();
      // Envoyer les configurations avec gestion des erreurs
    
    delay(500); // Délai entre les configurations
    
    if(!device.getHAConfig().sendSensorConfig("cuisine", "humidite", "humidity", "%", "Humidité Cuisine")) {
        Serial.println("Échec de la configuration du capteur d'humidité");
    }
        delay(500);

     if(!device.getHAConfig().sendSensorConfig("cuisine", "Temp", "temperature", "%", "Temp Cuisine")) {
        Serial.println("Échec de la configuration du capteur d'Temp");
    }
            delay(500);

    if(!device.getHAConfig().sendSensorConfig("cuisine", "temperature", "temperature", "°C", "Température Cuisine")) {
        Serial.println("Échec de la configuration du capteur de température");
    }
            delay(500);

     if(!device.getHAConfig().sendSensorConfig("cuisine", "popopopopo", "popopopopo", "xxl", "popopopopo Cuisine")) {
        Serial.println("Échec de la configuration du capteur de popopopopo");
    }
    
    
    delay(500);
    
    if(!device.getHAConfig().sendSwitchConfig("cuisine", "lampe", "Lampe Cuisine")) {
        Serial.println("Échec de la configuration de la lampe");
    }
}

void loop() {

    // Utilisation de handle() au lieu de loop()
    device.handle();
    
    // Simuler des données de capteurs
    static unsigned long lastSend = 0;
    if (millis() - lastSend > 5000) {
        float temp = random(200, 300) / 10.0;
        device.publishSensorData("cuisine", "Temp", temp);
        
        float hum = random(300, 800) / 10.0;
        device.publishSensorData("cuisine", "humidite", hum);
        
        lastSend = millis();
    }
}