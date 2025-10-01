
# import requests
# import board
# import adafruit_dht
# import RPi.GPIO as GPIO
# import time
# from datetime import datetime

# # Setup
# DHT_PIN = board.D17
# GAS_SENSOR_PIN = 4
# API_ENDPOINT = "http://127.0.0.1:5000/api/data"

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)

# buzzer = 23
# GPIO.setup(buzzer, GPIO.OUT)

# sensor = adafruit_dht.DHT22(DHT_PIN)

# try:
#     while True:
#         try:
#             temperature_c = sensor.temperature
#             humidity = sensor.humidity

#             # Handle cases where sensor returns None
#             if temperature_c is None or humidity is None:
#                 print("Sensor read failed. Retrying...")
#                 time.sleep(1)
#                 continue

#             gas_present = GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW
#             gas_state = "Gas Present" if gas_present else "No Gas"

#             payload = {
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "temperature_c": round(temperature_c, 1),
#                 "humidity": round(humidity, 1),
#                 "gas_state": gas_state
#             }

#             # Alert condition
#             if payload["temperature_c"] > 27.5 or gas_state == "Gas Present":
#                 # Beep 3 times as a warning
#                 for _ in range(3):
#                     GPIO.output(buzzer, GPIO.HIGH)
#                     print("Beep")
#                     time.sleep(0.5)
#                     GPIO.output(buzzer, GPIO.LOW)
#                     print("No Beep")
#                     time.sleep(0.5)

#             # Send to API
#             response = requests.post(API_ENDPOINT, json=payload)
#             print(f"Sent data: {payload}, Status: {response.status_code}")

#         except Exception as e:
#             print("Error:", e)

#         time.sleep(0.5)  # Wait before next read

# except KeyboardInterrupt:
#     print("Interrupted by user. Cleaning up...")

# finally:
#     GPIO.cleanup()
#     print("GPIO cleaned up.")

import socketio
import board, adafruit_dht, RPi.GPIO as GPIO
import time
from datetime import datetime

# Socket.IO client
sio = socketio.Client()
sio.connect("http://197.255.72.248:5000")

# Setup
DHT_PIN = board.D17
GAS_SENSOR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)
sensor = adafruit_dht.DHT22(DHT_PIN)

try:
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

            # Emit via Socket.IO
            sio.emit("sensor_data", payload)

            # Alert condition (local buzzer)
            if payload["temperature_c"] > 27.5 or gas_state == "Gas Present":
                for _ in range(3):
                    GPIO.output(buzzer, GPIO.HIGH)
                    time.sleep(0.3)
                    GPIO.output(buzzer, GPIO.LOW)
                    time.sleep(0.3)

            print("Sent data:", payload)

        except Exception as e:
            print("Error:", e)

        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
