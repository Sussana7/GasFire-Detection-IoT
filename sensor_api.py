from flask import Flask, jsonify
import board
import adafruit_dht
import RPi.GPIO as GPIO
import csv
from datetime import datetime

# === Setup ===
app = Flask(__name__)

DHT_PIN = board.D17
GAS_SENSOR_PIN = 4
LOG_FILE = "sensor_log.csv"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)

sensor = adafruit_dht.DHT22(DHT_PIN)

# === Live Read Endpoint ===
@app.route("/api/live", methods=["GET"])
def get_live_data():
    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        temperature_f = temperature_c * 9 / 5 + 32
        gas_present = GPIO.input(GAS_SENSOR_PIN) == GPIO.LOW
        gas_state = "Gas Present" if gas_present else "No Gas"

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_c": round(temperature_c, 1),
            "temperature_f": round(temperature_f, 1),
            "humidity": round(humidity, 1),
            "gas_state": gas_state
        }

        return jsonify(data)

    except RuntimeError as e:
        return jsonify({"error": "Sensor read error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

# === Log Read Endpoint ===
@app.route("/api/log", methods=["GET"])
def get_log_data():
    try:
        with open(LOG_FILE, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Log file not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to read log file", "details": str(e)}), 500

# === Run App ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
