import RPi.GPIO as GPIO
import time

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Sensor is ACTIVE LOW (0 when magnet is present)
        if GPIO.input(PIN) == False:
            print("Magnet detected!")
        else:
            print("No magnet.")
        
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
