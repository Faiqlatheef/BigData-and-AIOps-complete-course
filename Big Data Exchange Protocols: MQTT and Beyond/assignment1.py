import uuid
import paho.mqtt.client as mqtt
import json

# MQTT Broker Configuration
broker_address = "20.106.179.116"
broker_port = 1883
username = "server-mqtt"
password = "server-mqtt"

# Topics
sensor_data_topic = "D2S/SA/V1/digitest-A"
actuator_command_topic = "S2D/SA/V1/contest-A/A/0"
actuator_status_topic = "D2S/SA/V1/contest-A"

# Thresholds
temperature_threshold = 30  # Celsius
humidity_threshold = 60  # Percentage
battery_level_threshold = 250  # Arbitrary units

# Unique Client ID 
client_id = "assignment" + str(uuid.uuid4())[:8]  # Use first 8 characters of UUID


# Function to parse sensor data
def parse_sensor_data(payload):
    try:
        data = dict(item.split(":") for item in payload.decode().split(";"))
        temperature = int(data["0-T"])
        humidity = int(data["1-H"])
        return temperature, humidity
    except (ValueError, KeyError):
        print("Error parsing sensor data:", payload)
        return None, None


# Function to check thresholds and send command
def check_thresholds_and_send_command(temperature, humidity):
    if temperature > temperature_threshold or humidity > humidity_threshold:
        send_actuator_command(client, "OM:1")  # Turn on actuator
        print(f"Sensor readings exceeded thresholds. Sending turn-on command.")


# Function to parse actuator status
def parse_actuator_status(payload):
    try:
        data = json.loads(payload.decode())
        battery_level = data["0-B"]
        statuses = data["n-S"]  # Assuming "n" represents number of actuators
        return battery_level, statuses
    except (ValueError, KeyError):
        print("Error parsing actuator status:", payload)
        return None, None


# Function to check battery level and status change
def check_battery_and_status(battery_level, statuses, previous_statuses):
    if battery_level < battery_level_threshold:
        print(f"Warning: Battery level is low ({battery_level})!")

    for i, status in enumerate(statuses):
        if status != previous_statuses[i]:
            print(f"Actuator {i} status changed to {status}")
            previous_statuses[i] = status  # Update previous status


# Function to send actuator command
def send_actuator_command(client, command):
    client.publish(actuator_command_topic, command)
    print(f"Sent command to actuator: {command}")


# Function to store and retrieve previous actuator statuses (using a file)
def get_previous_status(index):
    try:
        with open("previous_statuses.json", "r") as f:
            data = json.load(f)
            return data.get(str(index))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def update_previous_status(index, status):
    previous_statuses = {}
    try:
        with open("previous_statuses.json", "r") as f:
            data = json.load(f)
            previous_statuses = data or {}
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    previous_statuses[str(index)] = status
    with open("previous_statuses.json", "w") as f:
        json.dump(previous_statuses, f)


# Create an MQTT client instance (moved outside functions)
client = mqtt.Client(client_id)
client.username_pw_set(username, password)

# MQTT Client Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        client.subscribe(sensor_data_topic)
        client.subscribe(actuator_status_topic)
    else:
        print("Failed to connect, return code %d\n" % rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
