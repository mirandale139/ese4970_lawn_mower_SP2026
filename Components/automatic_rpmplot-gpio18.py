import RPi.GPIO as GPIO
from gpiozero import Servo
import time
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ==========================================
# 1. Configuration & Setup
# ==========================================
SENSOR_PIN = 18
WHEEL_CIRCUMFERENCE_M = 1.05331  # meters per rotation

# Setup Sensor (RPi.GPIO)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup Motors (gpiozero)
left_wheel = Servo(13, min_pulse_width=1/1000, max_pulse_width=2/1000)
right_wheel = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

# ==========================================
# 2. Tracking Variables
# ==========================================
last_time = 0
rpm = 0.0
rps = 0.0
speed_mps = 0.0

# Lists to store data for plotting
time_data = []
rpm_data = []
rps_data = []
speed_data = []

# ==========================================
# 3. Sensor Interrupt Function
# ==========================================
def calculate_speed(channel):
    global last_time, rpm, rps, speed_mps
    
    current_time = time.time()
    if last_time != 0:
        delta_t = current_time - last_time
        if delta_t > 0.05: 
            rps = 1.0 / delta_t                       
            rpm = rps * 60.0                          
            speed_mps = rps * WHEEL_CIRCUMFERENCE_M   
            
    last_time = current_time

GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=calculate_speed, bouncetime=50)

# ==========================================
# 4. Main Control & Logging Loop
# ==========================================
print("Arming motors... (Ctrl+C to stop early)")
left_wheel.mid()
right_wheel.mid()

start_time = time.time()
current_motor_val = 0.0  # Tracks actual applied power for smooth ramping

try:
    while True:
        elapsed_time = time.time() - start_time
        
        # --- A. MOTOR CONTROL LOGIC ---
        # 1-minute automated run profile
        if elapsed_time < 3:
            target_val = 0.0   # Arming (3 seconds)
        elif elapsed_time < 18:
            target_val = 0.15  # Phase 1 speed
        elif elapsed_time < 33:
            target_val = 0.25  # Phase 2 speed
        elif elapsed_time < 48:
            target_val = 0.35  # Phase 3 speed
        elif elapsed_time < 63:
            target_val = 0.45  # Phase 4 speed
        else:
            print("1-minute test complete!")
            break # Exit loop to trigger the plotting
            
        # Slew rate limiter: Smoothly ramp up to the target speed to avoid jerking
        if current_motor_val < target_val:
            current_motor_val += 0.02  # Increase slowly every 0.5s
            if current_motor_val > target_val:
                current_motor_val = target_val
                
        # Apply the value to the motors
        if target_val == 0.0:
            left_wheel.mid()
            right_wheel.mid()
        else:
            # Safely apply the -2x multiplier for the left wheel, capping at -1.0
            left_val = max(-1.0, -2 * current_motor_val)
            right_wheel.value = current_motor_val
            left_wheel.value = left_val

        # --- B. SENSOR LOGIC ---
        # Reset speeds to 0 if no rotation is detected for 3 seconds
        if time.time() - last_time > 3 and rpm != 0:
            rpm, rps, speed_mps = 0.0, 0.0, 0.0
            
        # Print current status
        print(f"Time: {elapsed_time:04.1f}s | Target Power: {target_val*100:02.0f}% | RPM: {rpm:05.2f} | RPS: {rps:04.2f} | Speed: {speed_mps:04.2f} m/s")
        
        # Record the current data points for the plot
        time_data.append(elapsed_time)
        rpm_data.append(rpm)
        rps_data.append(rps)
        speed_data.append(speed_mps)
        
        time.sleep(0.5) 

except KeyboardInterrupt:
    print("\nTest interrupted early by user.")

finally:
    # ==========================================
    # 5. Safe Teardown & Plotting (Always Runs)
    # ==========================================
    print("\nStopping motors and cleaning up...")
    left_wheel.mid()
    right_wheel.mid()
    time.sleep(0.5)  # Let motors fully stop before detaching
    left_wheel.detach()
    right_wheel.detach()
    GPIO.cleanup()
    
    print("Generating plot...")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
    
    # Subplot 1: RPS (Top)
    ax1.plot(time_data, rps_data, color='tab:green', linewidth=2)
    ax1.set_ylabel('RPS')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_title('Wheel Metrics Over Time (Automated Ramp)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Subplot 2: RPM (Middle)
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
    
    plt.tight_layout()
    
    output_dir = os.path.expanduser("~/ESE4970/rpm_output_plots")
    os.makedirs(output_dir, exist_ok=True) 
    
    timestamp = datetime.now().strftime("%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"wheel_metrics_{timestamp}.png")
    
    plt.savefig(output_filename, dpi=300)
    print(f"Success! Plot saved to: {output_filename}")
