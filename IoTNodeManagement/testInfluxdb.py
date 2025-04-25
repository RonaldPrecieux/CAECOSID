import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from  datetime import datetime
token = os.environ.get("INFLUXDB_TOKEN")
org = "rolux-org"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="dommo-bucket"

write_api = client.write_api(write_options=SYNCHRONOUS)

# point = (
#     Point("temperature")             # Measurement
#     .tag("device", "esp32_abcd1234") # Tag
#     .tag("location", "salon")        # Tag
#     .field("value", 24.7)            # Field
#     .time(datetime.utcnow())         # Timestamp (automatique)
# )
# write_api.write(bucket=bucket, org="rolux-org", record=point)
# time.sleep(1) # separate points by 1 second

query_api = client.query_api()

query = """from(bucket: "dommo-bucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "iot_measurement")"""
tables = query_api.query(query, org="rolux-org")

for table in tables:
  for record in table.records:
    print(record)
