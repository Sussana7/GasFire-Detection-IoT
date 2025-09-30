# sensor_publisher.py
import requests
import board
import adafruit_dht
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Setup
DHT_PIN = board.D17
GAS_SENSOR_PIN = 4
API_ENDPOINT = "http://<your-server-ip>:5000/api/data"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)

sensor = adafruit_dht.DHT22(DHT_PIN)

while True:
    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        gas_present = GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW
        gas_state = "Gas Present" if gas_present else "No Gas"

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_c": round(temperature_c, 1),
            "humidity": round(humidity, 1),
            "gas_state": gas_state
        }

        response = requests.post(API_ENDPOINT, json=payload)
        print(f"Sent data: {payload}, Status: {response.status_code}")

    except Exception as e:
        print("Error:", e)

    time.sleep(10)  # Send every 10 seconds
