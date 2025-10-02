
from flask import Flask, request, jsonify, render_template, send_file
from flask_socketio import SocketIO, emit
import os, csv, io
import pandas as pd
import matplotlib.pyplot as plt
from config import Config
from email_utils import mail, send_alert
import base64

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

LOG_FILE = "sensor_log.csv"
latest_data = {}

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c", "humidity", "gas_state"])

@socketio.on("sensor_data")
def receive_data(sensor_data):
    global latest_data
    data = sensor_data
    latest_data = data

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            data["timestamp"],
            data["temperature_c"],
            data["humidity"],
            data["gas_state"]
        ])

    # 🚨 Send to frontend clients in real-time
    socketio.emit("sensor_update", data)
    socketio.emit("log_update", data) 
    req= "plot"
    socketio.emit("plot_request",req) 

    # Email alert
    if data['gas_state'] == 'Gas Present':
        subject = "⚠️ Gas Detected!"
        recipients = [os.getenv("HOMEOWNER_EMAIL")]
        body = f"Gas detected!\n\nTime: {data['timestamp']}\nTemp: {data['temperature_c']} °C\nHumidity: {data['humidity']} %"
        send_alert(subject, body, recipients)
       

    return jsonify({"message": "Data received"}), 200


@socketio.on("plot_request")
def plot_data(req):
    if req == "plot":
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
            image_base64 = base64.b64encode(buf.read()).decode("utf-8")
            socketio.emit("plot_image", {"image": image_base64})
            print(image_base64)

        except Exception as e:
                socketio.emit("plot_image", {"error": str(e)})


@app.route("/")
def dashboard():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)




# @app.route("/")
# def dashboard():
#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
