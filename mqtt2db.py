import paho.mqtt.client as mqtt
import mariadb
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

def insert(electricity_meter_name, reading, current_power, time):
    val = (electricity_meter_name, reading, current_power, time)
    cursor.execute(sql, val)
    connection.commit()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tele/Haus/SENSOR")
    client.subscribe("tele/Solar/SENSOR")


def on_message(client, userdata, msg):
    msg_json = json.loads(msg.payload)
    electricity_meter_name = msg.topic.split("/")[1]
    reading = msg_json[electricity_meter_name]["reading"]
    current_power = msg_json[electricity_meter_name]["current_power"]
    time = msg_json["Time"]
    insert(electricity_meter_name, reading, current_power, time)


connection = mariadb.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = connection.cursor()
sql = "INSERT INTO meter_readings (electricity_meter_name, reading, current_power, time) VALUES (%s, %s, %s, %s)"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(os.getenv('MQTT_HOST'), os.getenv('MQTT_PORT'), 60)

client.loop_forever()
