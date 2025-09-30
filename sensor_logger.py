import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import csv
import os
from datetime import datetime

# === GPIO & Sensor Setup ===
DHT_PIN = board.D17          # GPIO pin connected to DHT22
GAS_SENSOR_PIN = 4           # GPIO pin connected to MQ-2 digital output (DO)
BUZZER_PIN = 23              # GPIO pin connected to buzzer
LOG_FILE = "sensor_log.csv"  # CSV file path

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

sensor = adafruit_dht.DHT22(DHT_PIN)

# === CSV File Setup ===
def init_csv():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "temperature_c", "temperature_f", "humidity", "gas_state"
            ])

# === Read sensors and log to CSV ===
def read_and_log():
    try:
        # Read temperature and humidity
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        temperature_f = temperature_c * 9 / 5 + 32

        # Read gas sensor (LOW means gas detected)
        gas_present = GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW
        gas_state = "Gas Present" if gas_present else "No Gas"

        # Activate buzzer if gas detected
        GPIO.output(BUZZER_PIN, GPIO.HIGH if gas_present else GPIO.LOW)

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log to CSV
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, round(temperature_c, 1), round(temperature_f, 1),
                round(humidity, 1), gas_state
            ])

        print(f"[{timestamp}] Temp: {temperature_c:.1f}°C, Humidity: {humidity:.1f}%, Gas: {gas_state}")

    except RuntimeError as e:
        print("Sensor read error:", e)
    except Exception as e:
        print("Unexpected error:", e)

# === Main Loop ===
if __name__ == "__main__":
    print("Starting sensor logger... Press Ctrl+C to stop.")
    init_csv()
    try:
        while True:
            read_and_log()
            time.sleep(2)  # Adjust sampling rate here
    except KeyboardInterrupt:
        print("Exiting gracefully.")
    finally:
        sensor.exit()
        GPIO.cleanup()
