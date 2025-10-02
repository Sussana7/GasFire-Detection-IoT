import socketio
import board, adafruit_dht, RPi.GPIO as GPIO
import time
from datetime import datetime

# Socket.IO client
sio = socketio.Client()
sio.connect("http://127.0.0.1:8080")

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
