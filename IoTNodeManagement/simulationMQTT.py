import paho.mqtt.client as mqtt
import json
import random
import time
from threading import Thread

# Configuration MQTT
MQTT_BROKER = "localhost"  # Remplacez par l'adresse de votre broker
MQTT_PORT = 1883
BASE_TOPIC = "device"

# Liste des capteurs possibles
SENSORS = [
    "temperature",
    "co2",
    "presence",
    "fume",
    "acceleromete",
    "heart_rate"
]

# Données des pièces et MACs
ROOMS = {
    "Salon": ["2b5d53c2-4984-49ce-863e-1253feea2cc0","96d3d05f-4c6c-4b39-87dd-11a008fe34e2", "9aa404a5-38b4-48a1-b320-07538e59cc5d", "dd4a1ad4-9685-476f-9861-a1abc40005b6", "ede1aa46-3db3-4bc0-9b23-1d4c30dadbf4"],
    #"Chambre": ["25900a77-ca87-4656-a9b1-9863e1a8ac1b"],# "89f2e788-8c25-4c0a-86f9-c1c1e5fbbd94", "8021d654-f364-4228-b407-5049cec3cfc5", "9e3cee38-59f0-4771-a392-09b1d367872e", "6f7b8efb-35ec-40d2-91e5-9eba999381a6"],
    #"Garage": ["cac2b5e9-07dd-405f-95f2-283b373d09e9"], #"bd753ad0-0795-401d-be63-ba5d8fb74aad", "dd65ad6e-e566-4529-ad47-dfd81a320353", "91b84645-a94a-48eb-a29e-7279ce695801", "cec7e8e4-f769-40fa-8ef4-d8794075e22c"],
    #"Cuisine": ["5b6aa9b4-a075-4b4a-a780-016e6925b478"], #"05f0adcc-a397-402a-bd49-332413eac221", "e5d93799-c661-4d95-8441-00ac5240cfd2", "ac069ab2-dd07-4283-b1fb-afbc2f4ff16e", "bc8508e3-5f44-43b2-8103-c86f8cebeeb1"],
    #"Salle de Bain": ["398e4d92-2f3e-4a36-826b-0b05b48d76ff"],# "60f00bc2-6e73-43c9-909e-e9c2f5bb33ee", "fd77a6f8-1c63-478f-8b7f-b0a3f91562f4", "aefed077-d160-46ac-ae81-e8cfc7789066", "3ff91de8-ab87-4daf-ac18-16874722a7bb"],
    #"Salle a manger": ["6202dba1-74ec-432d-98d6-1edc3088198b"],# "bb1a18ac-723a-4626-ace0-2f0fe09785bb", "e88ea0e7-e157-4001-977d-78ee8c9af91e", "d0c2615b-0255-49ba-b911-48f6112093f1", "c666d61a-c8f5-4bb4-b17a-064752b72d2a"]
}

# Valeurs réalistes pour chaque capteur
def generate_sensor_data(sensor_type):
    if sensor_type == "temperature":
        return round(random.uniform(18.0, 30.0), 1)  # °C
    elif sensor_type == "co2":
        return random.randint(400, 2000)  # ppm
    elif sensor_type == "presence":
        return random.choice([0, 1])  # 0 ou 1
    elif sensor_type == "fume":
        return round(random.uniform(0.0, 1.0), 2)  # ratio 0-1
    elif sensor_type == "acceleromete":
        return {
            "x": round(random.uniform(-2.0, 2.0), 2),
            "y": round(random.uniform(-2.0, 2.0), 2),
            "z": round(random.uniform(-2.0, 2.0), 2)
        }
    elif sensor_type == "heart_rate":
        return random.randint(60, 120)  # bpm
    return None

# Fonction pour simuler un device
def simulate_device(mac, room_name):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    
    # Choisir 3 capteurs aléatoires pour ce device
    device_sensors = random.sample(SENSORS, 3)
    print(f"Device {mac} dans {room_name} surveille: {', '.join(device_sensors)}")
    
    while True:
        for sensor in device_sensors:
            topic = f"{BASE_TOPIC}/{mac}/{sensor}"
            payload = {
                "value": generate_sensor_data(sensor),
                "timestamp": int(time.time()),
                "room": room_name,
                "unit": get_unit(sensor)
            }
            client.publish(topic, json.dumps(payload))
        time.sleep(random.uniform(1.0, 5.0))  # Intervalle aléatoire entre 1-5s

def get_unit(sensor_type):
    units = {
        "temperature": "°C",
        "co2": "ppm",
        "presence": "bool",
        "fume": "ratio",
        "accelerometer_3axis": "m/s²",
        "heart_rate": "bpm"
    }
    return units.get(sensor_type, "unknown")

# Lancer un thread par device
def start_simulation():
    threads = []
    for room_name, macs in ROOMS.items():
        for mac in macs:
            t = Thread(target=simulate_device, args=(mac, room_name))
            t.start()
            threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    print("Démarrage de la simulation MQTT...")
    start_simulation()