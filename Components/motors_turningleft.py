from gpiozero import Servo
from time import sleep

# Setup pins
left_wheel = Servo(13, min_pulse_width=1/1000, max_pulse_width=2/1000)
right_wheel = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

try:
    print("Arming...")
    left_wheel.mid()
    right_wheel.mid()
    sleep(3)

    print("Turning Right (Pivot)...")
    for i in range(0, 21): 
        val = i / 100
        # Left wheel forward (-) and Right wheel backward (-)
        # Using your multiplier for the dominant wheel
        left_wheel.value = -2*val
        right_wheel.value = -2*val
        sleep(0.1)
    
    sleep(2)
    left_wheel.mid()
    right_wheel.mid()
    print("Stopped.")

except KeyboardInterrupt:
    left_wheel.detach()
    right_wheel.detach()
