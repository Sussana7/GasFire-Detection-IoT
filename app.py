# from dotenv import load_dotenv
# load_dotenv()  
# from flask import Flask, request, jsonify,render_template
# import csv
# import send_mail
# from config import Config  
# import os

# app = Flask(__name__)
# send_mail.mail.init_app(app)
# LOG_FILE = "sensor_log.csv"
# latest_data = {}  

# app.config.from_object(Config) 

# print("MAIL_DEFAULT_SENDER =", app.config.get("MAIL_DEFAULT_SENDER"))

# # Ensure log file exists with headers
# if not os.path.exists(LOG_FILE):
#     with open(LOG_FILE, "w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(["timestamp", "temperature_c", "humidity", "gas_state"])


# # Unified POST endpoint
# @app.route('/api/data', methods=['POST'])
# def receive_data():
#     global latest_data
#     data = request.get_json()
#     print("Received data:", data)

#     # Validate required fields
#     required = ["timestamp", "temperature_c", "humidity", "gas_state"]
#     if not all(k in data for k in required):
#         return jsonify({"error": "Missing fields"}), 400

#     latest_data = data  # Cache the latest reading

#     # Append data to CSV
#     with open(LOG_FILE, "a", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow([
#             data["timestamp"],
#             data["temperature_c"],
#             data["humidity"],
#             data["gas_state"]
#         ])

#     # Send email alert if gas is detected
#     if data['gas_state'] == 'Gas Present':
#         subject="⚠️ Gas Detected in Your Home!",
#         recipients=[os.getenv("HOMEOWNER_EMAIL")], 
#         body=(
#             f"Alert!\n\n"
#             f"Gas has been detected by your sensor setup.\n\n"
#             f"Time: {data['timestamp']}\n"
#             f"Temperature: {data['temperature_c']} °C\n"
#             f"Humidity: {data['humidity']} %\n\n"
#             f"Please take action immediately!"
#             )
#         send_mail.send_alert(subject,body,[recipients])
          

#     return jsonify({"message": "Data received"}), 200


# # GET endpoint — frontend fetches live data
# @app.route("/api/live", methods=["GET"])
# def get_live_data():
#     if not latest_data:
#         return jsonify({"error": "No data yet"}), 404
#     return jsonify(latest_data)

# # GET endpoint — read entire log
# @app.route("/api/log", methods=["GET"])
# def get_log():
#     try:
#         with open(LOG_FILE, "r") as file:
#             reader = csv.DictReader(file)
#             data = list(reader)
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
# @app.route("/")
# def dashboard():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

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
from email_utils import mail, send_alert  # ✅ Use renamed module

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)  # ✅ Initialize Flask-Mail properly

LOG_FILE = "sensor_log.csv"
latest_data = {}

print("MAIL_DEFAULT_SENDER =", app.config.get("MAIL_DEFAULT_SENDER"))

# Ensure log file exists with headers
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

    # ✅ FIXED: No trailing commas (which create tuples!)
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
        df = pd.read_csv(LOG_FILE)

        if df.empty or not all(col in df.columns for col in ["timestamp", "temperature_c", "humidity", "gas_state"]):
            return "No valid data to plot", 400

        # Convert timestamp column to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Drop rows where timestamp is NaT or other essential data missing
        df = df.dropna(subset=["timestamp", "temperature_c", "humidity"])

        # Convert gas state to binary
        df["gas_binary"] = df["gas_state"].apply(lambda x: 1 if x == "Gas Present" else 0)

        # Use a nicer style
        plt.style.use("seaborn-darkgrid")

        fig, ax1 = plt.subplots(figsize=(10, 5))
        fig.autofmt_xdate(rotation=45)

        ax1.set_title("Sensor Data Over Time", fontsize=14)
        ax1.set_xlabel("Time", fontsize=12)
        ax1.set_ylabel("Temperature / Humidity", fontsize=12)

        # Plot temperature and humidity with markers and lines
        ax1.plot(
            df["timestamp"],
            df["temperature_c"],
            label="Temperature (°C)",
            color="tomato",
            linestyle="-",
            marker="o",
            markersize=4,
            linewidth=2
        )
        ax1.plot(
            df["timestamp"],
            df["humidity"],
            label="Humidity (%)",
            color="steelblue",
            linestyle="--",
            marker="s",
            markersize=4,
            linewidth=2
        )

        # Second y-axis for gas presence
        ax2 = ax1.twinx()
        ax2.plot(
            df["timestamp"],
            df["gas_binary"],
            label="Gas Detected",
            color="green",
            linestyle="-.",
            marker="^",
            markersize=4,
            linewidth=1.5,
            alpha=0.8
        )
        ax2.set_ylabel("Gas Presence (1 = Yes)", fontsize=12)

        # Grid
        ax1.grid(True, which="major", linestyle="--", linewidth=0.5, color="gray", alpha=0.7)

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)
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
