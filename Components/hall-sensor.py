from gpiozero import DigitalInputDevice
from signal import pause

# Initialize the sensor on GPIO 18
# pull_up=True uses the Pi's internal resistor to keep the signal steady
hall_sensor = DigitalInputDevice(18, pull_up=True)

def magnet_detected():
    print("Magnet detected!")

def magnet_removed():
    print("Magnet removed.")

# Assign functions to events
hall_sensor.when_activated = magnet_removed  # Signal goes HIGH (1)
hall_sensor.when_deactivated = magnet_detected # Signal goes LOW (0)

print("Reading Hall Effect Sensor... Press Ctrl+C to exit.")

try:
    pause() # Keeps the script running to listen for events
except KeyboardInterrupt:
    print("\nScript stopped by user.")
