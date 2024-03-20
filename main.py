import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Broker
broker = "test.mosquito.org"
port = 1883

client = mqtt.Client()
# MQTT topic pattern
course_code = "CS101"
name = "John_Doe"
topic_base = f"{course_code}/{name.replace(' ', '_')}"

# Current location and temperature
current_location = {"latitude": 0.0, "longitude": 0.0}
current_temperature = 0

# Function to connect to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(topic_base + "/my_temperature")

# Function to handle incoming MQTT messages
def on_message(client, userdata, msg):
    global current_temperature
    payload = json.loads(msg.payload)
    current_temperature = payload["temperature"]

# Function to publish Geojson message
def publish_geojson(client):
    global current_location, current_temperature
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [current_location["longitude"], current_location["latitude"]]
        },
        "properties": {
            "temperature": current_temperature
        }
    }
    client.publish(topic_base + "/my_temperature", json.dumps(geojson))

# Function to simulate location update
def update_location():
    global current_location
    while True:
        current_location["latitude"] = round(random.uniform(-90, 90), 6)
        current_location["longitude"] = round(random.uniform(-180, 180), 6)
        time.sleep(10)  # Update location every 10 seconds

# MQTT Client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Start MQTT client
client.connect(broker, port, 60)
client.loop_start()

# Simulate location update
update_location()
