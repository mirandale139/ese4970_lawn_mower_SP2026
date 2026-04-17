import RPi.GPIO as GPIO
import time

# Configuration
PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to track time
last_time = 0
rpm = 0

def calculate_speed(channel):
    global last_time, rpm
    
    # Get current time in seconds
    current_time = time.time()
    
    if last_time != 0:
        # Time taken for one full rotation
        delta_t = current_time - last_time
        
        # Avoid division by zero and extreme noise
        if delta_t > 0.05: 
            rpm = 60 / delta_t
            print(f"Rotation detected! Speed: {rpm:.2f} RPM")
            
    last_time = current_time

# Add an event listener for the falling edge (when magnet pulls signal to LOW)
# bouncetime=50 ignores accidental double-triggers within 50ms
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=calculate_speed, bouncetime=50)

print("Wheel Speed Monitor Started. Spin the wheel! (Ctrl+C to stop)")

try:
    while True:
        # If the wheel stops, the interrupt won't fire. 
        # We check if the last detection was more than 3 seconds ago to reset RPM to 0.
        if time.time() - last_time > 3 and rpm != 0:
            rpm = 0
            print("Wheel stopped. Speed: 0 RPM")
            
        time.sleep(1) 

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
