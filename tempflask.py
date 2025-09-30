# app.py
from flask import Flask, request, jsonify,render_template
import csv
import os

app = Flask(__name__)

LOG_FILE = "sensor_log.csv"
latest_data = {}  # In-memory cache for latest reading

# Create CSV if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c", "humidity", "gas_state"])

# POST endpoint — receives data from Pi
@app.route("/api/data", methods=["POST"])
def receive_data():
    global latest_data
    data = request.get_json()

    # Validate required fields
    required = ["timestamp", "temperature_c", "humidity", "gas_state"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    latest_data = data  # Cache the latest data

    # Append to CSV
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            data["timestamp"],
            data["temperature_c"],
            data["humidity"],
            data["gas_state"]
        ])

    return jsonify({"message": "Data received"}), 200

# GET endpoint — frontend fetches live data
@app.route("/api/live", methods=["GET"])
def get_live_data():
    if not latest_data:
        return jsonify({"error": "No data yet"}), 404
    return jsonify(latest_data)

# GET endpoint — read entire log
@app.route("/api/log", methods=["GET"])
def get_log():
    try:
        with open(LOG_FILE, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
