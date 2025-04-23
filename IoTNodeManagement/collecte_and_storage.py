import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from datetime import datetime
import logging

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "device/+/+"  # Wildcard pour tous les devices et capteurs

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "supersecrettoken"
INFLUX_ORG = "rolux-org"
INFLUX_BUCKET = "dommo-bucket"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MQTT-InfluxDB")

class InfluxDBWriter:
    def __init__(self):
        self.client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        
    def write_data(self, mac, sensor_type, value, room, unit):
        point = Point("iot_measurement") \
            .tag("device", mac) \
            .tag("sensor", sensor_type) \
            .tag("room", room) \
            .field("value", value) \
            .time(datetime.utcnow())
            
        try:
            self.write_api.write(bucket=INFLUX_BUCKET, record=point)
            logger.debug(f"Written to InfluxDB: {mac}/{sensor_type} = {value}{unit}")
        except Exception as e:
            logger.error(f"InfluxDB write error: {str(e)}")
    
    def __del__(self):
        self.client.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        mac = topic_parts[1]
        sensor_type = topic_parts[2]
        payload = json.loads(msg.payload.decode())
        
        # Validation des données
        required_fields = {'value', 'timestamp', 'room', 'unit'}
        if not all(field in payload for field in required_fields):
            raise ValueError("Invalid payload structure")
        
        # print('Pret pour le stockage')
        # Écriture dans InfluxDB
        influx_writer.write_data(
            mac=mac,
            sensor_type=sensor_type,
            value=payload['value'],
            room=payload['room'],
            unit=payload['unit']
        )
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
    except ValueError as e:
        logger.error(f"Data validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Initialisation InfluxDB
    influx_writer = InfluxDBWriter()
    
    # Configuration MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        logger.info("Starting MQTT listener...")
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"MQTT connection error: {str(e)}")
    finally:
        mqtt_client.disconnect()