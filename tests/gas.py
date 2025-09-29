
import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for reading the DO output
DO_PIN = 7  # Replace with the actual GPIO pin number
GPIO.setup(DO_PIN, GPIO.IN)

try:
    while True:
        # Read the state of the DO pin
        gas_present = GPIO.input(DO_PIN)

        # Determine if gas is present or not
        if gas_present == GPIO.LOW:
            gas_state = "Gas Present"
        else:
            gas_state = "No Gas"

        # Print the gas state
        print(f"Gas State: {gas_state}")

        time.sleep(0.5)  # Wait for a short period before reading again

except KeyboardInterrupt:
    print("Gas detection stopped by user")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()