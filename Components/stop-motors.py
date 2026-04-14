from gpiozero import PWMOutputDevice, Servo
import RPi.GPIO as GPIO

# Method 1: The 'Clean' way using gpiozero
try:
    s1 = PWMOutputDevice(13)
    s2 = PWMOutputDevice(12)
    s1.value = 0
    s2.value = 0
    s1.close()
    s2.close()
except:
    pass

# Method 2: The 'Brute Force' way to ensure pins are dead
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.cleanup()

print("Signals killed. If they are still spinning, pull the battery or the S1/S2 wires.")
