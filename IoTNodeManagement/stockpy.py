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
print("=====Welcome======")

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
        
    def write_data(self, mac, sensor_type, payload):
        point = Point("iot_measurement")
        
        # Add tags
        point.tag("device", mac)
        point.tag("sensor", sensor_type)
        point.tag("room", payload.get("room", "unknown"))
        
        # Handle different sensor types appropriately
        value = payload['value']
        
        if sensor_type == "accelerometer_3axis":
            # Split dictionary into separate fields
            if isinstance(value, dict):
                point.field("accel_x", float(value.get('x', 0)))
                point.field("accel_y", float(value.get('y', 0)))
                point.field("accel_z", float(value.get('z', 0)))
            else:
                logger.warning(f"Invalid accelerometer data from {mac}")
                return
        else:
            # Convert all other values to float
            try:
                point.field("value", float(value))
            except (ValueError, TypeError):
                logger.warning(f"Invalid numeric value from {mac} for {sensor_type}")
                return
        
        try:
            self.write_api.write(bucket=INFLUX_BUCKET, record=point)
            logger.debug(f"Written: {mac}/{sensor_type}")
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
        
        # Validate required fields
        if 'value' not in payload:
            raise ValueError("Missing 'value' in payload")
        
        # Write to InfluxDB
        # influx_writer.write_data(mac, sensor_type, payload)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
    except ValueError as e:
        logger.error(f"Data validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    influx_writer = InfluxDBWriter()
    
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