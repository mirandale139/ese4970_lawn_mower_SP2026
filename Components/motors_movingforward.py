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

    print("Ramping Both Wheels Forward...")
    # We use a loop to slowly increase power to BOTH wheels
    for i in range(0, 21): # 0% to 20%
        val = i / 100
        left_wheel.value = -2*val
        right_wheel.value = val
        sleep(0.1)
    
    print("Moving...")
    sleep(2)

    left_wheel.mid()
    right_wheel.mid()
    print("Stopped.")

except KeyboardInterrupt:
    left_wheel.detach()
    right_wheel.detach()
