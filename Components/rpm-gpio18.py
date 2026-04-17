import RPi.GPIO as GPIO
import time

# Configuration
PIN = 18
WHEEL_CIRCUMFERENCE_M = 1.05331  # meters per rotation

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to track time and speed
last_time = 0
rpm = 0.0
rps = 0.0  # Added RPS variable
speed_mps = 0.0

def calculate_speed(channel):
    global last_time, rpm, rps, speed_mps
    
    # Get current time in seconds
    current_time = time.time()
    
    if last_time != 0:
        # Time taken for one full rotation
        delta_t = current_time - last_time
        
        # Avoid division by zero and extreme noise
        if delta_t > 0.05: 
            rps = 1.0 / delta_t                       # Calculate Rotations Per Second
            rpm = rps * 60.0                          # Calculate Revolutions Per Minute
            speed_mps = rps * WHEEL_CIRCUMFERENCE_M   # Calculate Linear Speed
            
    last_time = current_time

# Add an event listener for the falling edge (when magnet pulls signal to LOW)
# bouncetime=50 ignores accidental double-triggers within 50ms
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=calculate_speed, bouncetime=50)

print("Wheel Speed Monitor Started. Spin the wheel! (Ctrl+C to stop)")

try:
    while True:
        # If the wheel stops, the interrupt won't fire. 
        # We check if the last detection was more than 3 seconds ago to reset.
        if time.time() - last_time > 3 and rpm != 0:
            rpm = 0.0
            rps = 0.0
            speed_mps = 0.0
            print("Wheel stopped.")
            
        # Print the data at a set frequency (e.g., twice a second)
        print(f"RPM: {rpm:.2f} | RPS: {rps:.2f} | Speed: {speed_mps:.2f} m/s")
        
        # Adjust this sleep time to change how often it prints (0.5 = every half second)
        time.sleep(0.5) 

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
