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
        # Right wheel forward (+) and Left wheel backward (+)
        # Adjusting the 2* multiplier based on your discovery
        left_wheel.value = val 
        right_wheel.value = val 
        sleep(0.1)
    
    sleep(2)
    left_wheel.mid()
    right_wheel.mid()
    print("Stopped.")

except KeyboardInterrupt:
    left_wheel.detach()
    right_wheel.detach()
