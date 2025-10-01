from dotenv import load_dotenv
load_dotenv()
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from flask import send_file
from flask import Flask, request, jsonify, render_template
import csv
from config import Config
import os
from email_utils import mail, send_alert  

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app) 

LOG_FILE = "sensor_log.csv"
latest_data = {}

print("MAIL_DEFAULT_SENDER =", app.config.get("MAIL_DEFAULT_SENDER"))

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c", "humidity", "gas_state"])


@app.route('/api/data', methods=['POST'])
def receive_data():
    global latest_data
    data = request.get_json()
    print("Received data:", data)

    required = ["timestamp", "temperature_c", "humidity", "gas_state"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    latest_data = data

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            data["timestamp"],
            data["temperature_c"],
            data["humidity"],
            data["gas_state"]
        ])

    if data['gas_state'] == 'Gas Present':
        subject = "⚠️ Gas Detected in Your Home!"
        recipients = [os.getenv("HOMEOWNER_EMAIL")]
        body = (
            f"Alert!\n\n"
            f"Gas has been detected by your sensor setup.\n\n"
            f"Time: {data['timestamp']}\n"
            f"Temperature: {data['temperature_c']} °C\n"
            f"Humidity: {data['humidity']} %\n\n"
            f"Please take action immediately!"
        )

        send_alert(subject, body, recipients)

    return jsonify({"message": "Data received"}), 200


@app.route("/api/live", methods=["GET"])
def get_live_data():
    if not latest_data:
        return jsonify({"error": "No data yet"}), 404
    return jsonify(latest_data)


@app.route("/api/log", methods=["GET"])
def get_log():
    try:
        with open(LOG_FILE, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/plot")
def plot_data():
    try:
        df = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])

        if df.empty or not all(col in df.columns for col in ["timestamp", "temperature_c", "humidity", "gas_state"]):
            return "No valid data to plot", 400

        # Convert gas_state to binary (0/1)
        df["gas_binary"] = df["gas_state"].apply(lambda x: 1 if x == "Gas Present" else 0)

        plt.style.use("default")  

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Sensor Data Over Time", fontsize=16, weight="bold")

        ax.plot(df["timestamp"], df["temperature_c"],
                label="Temperature (°C)", color="red", linewidth=2.5)

        ax.plot(df["timestamp"], df["humidity"],
                label="Humidity (%)", color="blue", linewidth=2.5)

        # Scale gas to stand out (0 or 100 instead of 0/1)
        ax.plot(df["timestamp"], df["gas_binary"] * 100,
                label="Gas Presence", color="green", linewidth=2.5)

        # Axis labels
        ax.set_xlabel("Time", fontsize=12, weight="bold")
        ax.set_ylabel("Values", fontsize=12, weight="bold")

        # Light grid
        ax.grid(True, linestyle="--", alpha=0.6)

        # Format time labels
        fig.autofmt_xdate()

        # Legend
        ax.legend(loc="upper left", fontsize=11)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        return f"Error generating plot: {e}", 500



@app.route("/")
def dashboard():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
