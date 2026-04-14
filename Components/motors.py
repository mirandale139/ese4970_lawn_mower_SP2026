from gpiozero import Servo
from time import sleep

# Setup pins with your verified pulse widths
left_wheel = Servo(13, min_pulse_width=1/1000, max_pulse_width=2/1000)
right_wheel = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

def stop_motors():
    """Safety function to bring wheels to neutral."""
    left_wheel.mid()
    right_wheel.mid()

def move_robot(direction, duration=2):
    print(f"\n--- Action: {direction.upper()} ---")
    
    # RAMP UP to 20% power to prevent "Broken Pipe" (Pi crashing)
    for i in range(0, 21):
        val = i / 100
        
        if direction == "forward":
            left_wheel.value = -2 * val
            right_wheel.value = val
        elif direction == "backward":
            left_wheel.value = val
            right_wheel.value = -2 * val
        elif direction == "left":
            left_wheel.value = 2 * val
            right_wheel.value = 2 * val
        elif direction == "right":
            left_wheel.value = -2*val
            right_wheel.value = -2*val
            
        sleep(0.05)

    print("Steady state...")
    sleep(duration)

    # RAMP DOWN to prevent inductive kickback/voltage spikes
    print("Ramping down...")
    for i in range(20, -1, -1):
        val = i / 100
        # Re-apply same logic for the ramp down
        if direction == "forward":
            left_wheel.value = -2 * val
            right_wheel.value = val
        elif direction == "backward":
            left_wheel.value = val
            right_wheel.value = -2 * val
        elif direction == "left":
            left_wheel.value = 2 * val
            right_wheel.value = 2 * val
        elif direction == "right":
            left_wheel.value = -2*val
            right_wheel.value = -2*val
        sleep(0.05)
    
    stop_motors()

# Main Execution
try:
    print("Initializing... Ensuring Sabertooth sees Neutral.")
    stop_motors()
    sleep(3)

    # Sequence of tests
    move_robot("forward")
    sleep(1)
    
    move_robot("backward")
    sleep(1)
    
    move_robot("left")
    sleep(1)
    
    move_robot("right")
    
    print("\n--- All tests complete! ---")

except KeyboardInterrupt:
    print("\nEmergency Stop Triggered.")
finally:
    left_wheel.detach()
    right_wheel.detach()
