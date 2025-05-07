import paho.mqtt.client as mqtt
import time
import random
import json

# Configuration
MAC = "AABBCCDDEEFF"  # Remplacer par la MAC de l'ESP32
BROKER_IP = "127.0.0.1"  # IP du broker MQTT
SALON_TOPIC_BASE = f"home/salon/esp32-{MAC}"
HOME_TOPIC_BASE = f"home/esp32-{MAC}"
CUISINE_TOPIC_BASE = f"home/cuisine/esp32-{MAC}"

# Callback pour les commandes reçues
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    if "lampe_salon/set" in topic:
        print(f"Commande lampe salon: {payload}")
        # Publier le nouveau state (ex: "ON" ou "OFF")
        client.publish(f"{SALON_TOPIC_BASE}/lampe_salon/state", payload, retain=True)
    
    elif "prise_tele/set" in topic:
        print(f"Commande prise télé: {payload}")
        client.publish(f"{SALON_TOPIC_BASE}/prise_tele/state", payload, retain=True)
    
    elif "ventilo/set" in topic:
        print(f"Commande ventilateur: {payload}")
        client.publish(f"{SALON_TOPIC_BASE}/ventilo/state", payload, retain=True)

    elif "alerte/set" in topic:
        print(f"Commande alerte: {payload}")
        client.publish(f"{HOME_TOPIC_BASE}/alerte/state", payload, retain=True)

# Envoi des configs Home Assistant 
def send_discovery(client):
    #======SALON======
    # Capteurs
    client.publish(
        "homeassistant/sensor/salon_temperature/config",
        json.dumps({
            "name": "Température Salon",
            "device_class": "temperature",
            "state_topic": f"{SALON_TOPIC_BASE}/temperature/state",
            "unit_of_measurement": "°C",
            "unique_id": f"esp32_{MAC}_temp"
        }),
        retain=True
    )
    
    client.publish(
        "homeassistant/sensor/humidite_salon/config",
        json.dumps({
            "name": "Humidité Salon",
            "device_class": "temperature",
            "state_topic": f"{SALON_TOPIC_BASE}/humidite/state",
            "unit_of_measurement": "%",
            "unique_id": f"esp32_{MAC}_hum"
        }),
        retain=True
    )
    
    client.publish(
        "homeassistant/sensor/salon_Gaz/config",
        json.dumps({
            "name": "Gaz Salon",
            "state_topic": f"{SALON_TOPIC_BASE}/gaz/state",
            "unit_of_measurement": "ppm",
            "unique_id": f"esp32_{MAC}_Gaz"
        }),
        retain=True
    )
    
    client.publish(
        "homeassistant/binary_sensor/salon_presence/config",
        json.dumps({
            "name": "Présence Salon",
            "device_class": "motion",
            "state_topic": f"{SALON_TOPIC_BASE}/presence/state",
            "unique_id": f"esp32_{MAC}_presence"
        }),
        retain=True
    )
    
    # Actionneurs
    client.publish(
        "homeassistant/light/lampe_salon/config",
        json.dumps({
            "name": "Lampe Salon",
            "command_topic": f"{SALON_TOPIC_BASE}/lampe_salon/set",
            "state_topic": f"{SALON_TOPIC_BASE}/lampe_salon/state",
            "unique_id": f"esp32_{MAC}_lampe"
        }),
        retain=True
    )
    
    client.publish(
        "homeassistant/switch/prise_tele/config",
        json.dumps({
            "name": "Prise Télé",
            "command_topic": f"{SALON_TOPIC_BASE}/prise_tele/set",
            "state_topic": f"{SALON_TOPIC_BASE}/prise_tele/state",
            "unique_id": f"esp32_{MAC}_prise"
        }),
        retain=True
    )
    
    client.publish(
        "homeassistant/switch/ventilo/config",
        json.dumps({
            "name": "Ventilateur Salon",
            "command_topic": f"{SALON_TOPIC_BASE}/ventilo/set",
            "state_topic": f"{SALON_TOPIC_BASE}/ventilo/state",
            "unique_id": f"esp32_{MAC}_ventilo"
        }),
        retain=True
    )
#====Maison Base ====
#Capteur
#Actionneur
    client.publish(
        "homeassistant/switch/alerte/config",
        json.dumps({
            "name": "Alerte",
            "command_topic": f"{HOME_TOPIC_BASE}/alerte/set",
            "state_topic": f"{HOME_TOPIC_BASE}/alerte/state",
            "unique_id": f"esp32_{MAC}_alerte"
        }),
        retain=True
    )

# Simulation des capteurs
def simulate_sensors(client):
    while True:
        # Température (20-25°C)
        temp = round(random.uniform(20.0, 30.0), 1)
        client.publish(f"{SALON_TOPIC_BASE}/temperature/state", temp)

        # humidité (20-25°C)
        hum = round(random.uniform(20.0, 80.0), 1)
        client.publish(f"{SALON_TOPIC_BASE}/humidite/state", hum)
        
        # CO2 (400-1000 ppm)
        gazSalon = random.randint(400, 1000)
        client.publish(f"{SALON_TOPIC_BASE}/gaz/state", gazSalon)
        
        # Présence (aléatoire: "ON" ou "OFF")
        presence = "ON" if random.random() > 0.7 else "OFF"
        client.publish(f"{SALON_TOPIC_BASE}/presence/state", presence)
        
        
        time.sleep(5)  # Toutes les 5 secondes

# Main
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER_IP, 1883, 60)

# S'abonner aux topics de commande
client.subscribe(f"{SALON_TOPIC_BASE}/+/set")
client.subscribe(f"{HOME_TOPIC_BASE}/+/set")

send_discovery(client)  # Envoi des configs

client.loop_start()
simulate_sensors(client)