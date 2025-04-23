import requests
import random
import json
import uuid

# Définir l'URL de base de l'API
BASE_URL = "http://localhost:8000"  # Remplace par l'URL de ton API

# Liste des noms de lieux possibles
lieux_names = ["Chambre", "Salon", "Garage", "Cuisine", "Salle de Bain","Salle a manger"]

# Générer des UUID pour les microcontrôleurs
def generate_uuid():
    # Générer un UUID pour ESP32 (en utilisant une version basée sur le MAC adresse ou simplement un UUID standard)
    return str(uuid.uuid4())

# Créer un lieu
def create_lieu(nom):
    url = f"{BASE_URL}/lieux/"
    data = {
        "nom": nom
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Lieu '{nom}' créé avec succès.")
        return response.json()
    else:
        print(f"Erreur lors de la création du lieu '{nom}': {response.json()}")
        return None

# Créer un microcontrôleur
def create_lieu(nom):
    response = requests.post(f"{BASE_URL}/lieux/", json={"nom": nom})
    if response.status_code == 200:
        print(f"Lieu '{nom}' créé avec succès.")
        return response.json()
    else:
        print(f"Erreur lors de la création du lieu '{nom}':")
        print(f"Status code: {response.status_code}")
        print(f"Contenu brut: {response.text}")
        return None
    
def formatlieujson(nom):
    response = requests.get(f"{BASE_URL}/lieux/nom/{nom}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la création du lieu '{nom}':")
        print(f"Status code: {response.status_code}")
        print(f"Contenu brut: {response.text}")
        return None

# Créer un microcontrôleur
def create_microcontrôleur(uuid, nom, lieu_id):
    url = f"{BASE_URL}/microcontroleurs/"
    data = {
        "uuid": uuid,
        "nom": nom,
        "lieu_id": lieu_id
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Microcontrôleur {nom} avec UUID {uuid} créé avec succès.")
    else:
        print(f"Erreur lors de la création du microcontrôleur {nom}: {response.json()}")


# Fonction pour envoyer beaucoup de données
def send_bulk_data():
    # Créer plusieurs lieux
    lieux = []
    for lieu_name in lieux_names:
        lieu = create_lieu(lieu_name)
        if lieu:
            lieux.append(lieu)

    # Créer des microcontrôleurs pour chaque lieu
    for lieu in lieux:
        lieu_id = lieu['id']
        # Générer plusieurs microcontrôleurs pour chaque lieu
        for i in range(5):  # Exemple : créer 5 microcontrôleurs par lieu
            micro_uuid = generate_uuid()
            micro_name = f"Micro_{lieu['nom']}_{i+1}"
            create_microcontrôleur(micro_uuid, micro_name, lieu_id)

# Appeler la fonction pour envoyer les données en masse
send_bulk_data()
