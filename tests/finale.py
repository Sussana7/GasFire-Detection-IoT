import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# DHT22 sensor setup
sensor = adafruit_dht.DHT22(board.D17)

# Gas sensor digital output pin (DO)
DO_PIN = 4
GPIO.setup(DO_PIN, GPIO.IN)

# Buzzer pin setup
BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    while True:
        try:
            temperature_c = sensor.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = sensor.humidity

            gas_present = GPIO.input(DO_PIN)

            if gas_present == GPIO.LOW:
                gas_state = "Gas Present"
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                print("Beep! Gas detected.")
            else:
                gas_state = "No Gas"
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                print("No gas. Buzzer off.")

            print("==============================================")
            print(f"Gas State: {gas_state}")
            print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(
                temperature_c, temperature_f, humidity))
            print("==============================================")

        except RuntimeError as error:
            print(f"DHT22 error: {error.args[0]}")
            time.sleep(2.0)
            continue

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    sensor.exit()
    GPIO.cleanup()
