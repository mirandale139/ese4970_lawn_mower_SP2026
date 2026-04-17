import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuration
PIN = 18
WHEEL_CIRCUMFERENCE_M = 1.05331  # meters per rotation

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to track time and speed
last_time = 0
rpm = 0.0
rps = 0.0
speed_mps = 0.0

# Lists to store data for plotting
time_data = []
rpm_data = []
rps_data = []
speed_data = []

def calculate_speed(channel):
    global last_time, rpm, rps, speed_mps
    
    # Get current time in seconds
    current_time = time.time()
    
    if last_time != 0:
        # Time taken for one full rotation
        delta_t = current_time - last_time
        
        # Avoid division by zero and extreme noise
        if delta_t > 0.05: 
            rps = 1.0 / delta_t                       
            rpm = rps * 60.0                          
            speed_mps = rps * WHEEL_CIRCUMFERENCE_M   
            
    last_time = current_time

# Add an event listener for the falling edge
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=calculate_speed, bouncetime=50)

print("Wheel Speed Monitor Started. Spin the wheel! (Ctrl+C to stop and generate plot)")

# Record the start time so the X-axis starts at 0
start_time = time.time()

try:
    while True:
        # Reset speeds to 0 if no rotation is detected for 3 seconds
        if time.time() - last_time > 3 and rpm != 0:
            rpm = 0.0
            rps = 0.0
            speed_mps = 0.0
            print("Wheel stopped.")
            
        print(f"RPM: {rpm:.2f} | RPS: {rps:.2f} | Speed: {speed_mps:.2f} m/s")
        
        # Record the current data points
        current_elapsed_time = time.time() - start_time
        time_data.append(current_elapsed_time)
        rpm_data.append(rpm)
        rps_data.append(rps)
        speed_data.append(speed_mps)
        
        # Adjust sleep to control logging frequency (0.5s = 2Hz)
        time.sleep(0.5) 

except KeyboardInterrupt:
    print("\nStopping monitor and cleaning up GPIO...")
    GPIO.cleanup()
    
    print("Generating plot...")
    
    # Create a figure with 3 subplots (sharex removed due to different time units)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
    
    # Subplot 1: RPS (Top)
    ax1.plot(time_data, rps_data, color='tab:green', linewidth=2)
    ax1.set_ylabel('RPS')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_title('Wheel Metrics Over Time')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Subplot 2: RPM (Middle - Converted to minutes for X-axis)
    time_data_mins = [t / 60.0 for t in time_data]
    ax2.plot(time_data_mins, rpm_data, color='tab:red', linewidth=2)
    ax2.set_ylabel('RPM')
    ax2.set_xlabel('Time (minutes)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Subplot 3: Linear Speed (Bottom)
    ax3.plot(time_data, speed_data, color='tab:blue', linewidth=2)
    ax3.set_ylabel('Speed (m/s)')
    ax3.set_xlabel('Time (seconds)')
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout so labels don't overlap
    plt.tight_layout()
    
    # Setup directory and save
    output_dir = os.path.expanduser("~/ESE4970/rpm_output_plots")
    os.makedirs(output_dir, exist_ok=True)  # Creates the folder safely if it doesn't exist
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"wheel_metrics_{timestamp}.png")
    
    plt.savefig(output_filename, dpi=300)
    print(f"Success! Plot saved to: {output_filename}")
