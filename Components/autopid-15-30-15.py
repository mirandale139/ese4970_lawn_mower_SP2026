import RPi.GPIO as GPIO
from gpiozero import Servo
import time
import matplotlib.pyplot as plt
import os
import csv
from datetime import datetime

# ==========================================
# 1. Configuration & Setup
# ==========================================
SENSOR_PIN = 18
WHEEL_CIRCUMFERENCE_M = 1.05331  # meters per rotation

# --- PID Controller Constants ---
# TUNE THESE! Start with Kp and Ki. 
Kp = 0.15  # Proportional: reacts to current error
Ki = 0.60  # Integral: builds up to hold steady state power
Kd = 0.02  # Derivative: dampens sudden changes

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

time_data, rpm_data, rps_data, speed_data, target_speed_data = [], [], [], [], []

# Create directories
output_dir = os.path.expanduser("~/ESE4970/rpm_output_plots")
os.makedirs(output_dir, exist_ok=True) 

# Generate timestamps for files
timestamp = datetime.now().strftime("%m%d_%H%M%S")
csv_filename = os.path.join(output_dir, f"wheel_data_{timestamp}.csv")
plot_filename = os.path.join(output_dir, f"wheel_metrics_{timestamp}.png")

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
last_pid_time = time.time()

# PID state variables
integral = 0.0
prev_error = 0.0

# Open CSV File for writing
with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Time_s', 'Target_Speed_mps', 'Actual_Speed_mps', 'Target_Power_Pct', 'RPM', 'RPS'])

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            dt = current_time - last_pid_time
            last_pid_time = current_time
            
            # --- A. STEPPED TARGET SPEED PROFILE (2 Minutes) ---
            if elapsed_time < 3:
                target_speed = 0.0   
            elif elapsed_time < 42:
                target_speed = 0.90  # Target roughly equivalent to 15%
            elif elapsed_time < 81:
                target_speed = 1.45  # Target roughly equivalent to 45%
            elif elapsed_time < 120:
                target_speed = 0.90  
            elif elapsed_time < 125:
                target_speed = 0.0
            else:
                print("2-minute PID step test complete!")
                break
                
            # --- B. PID CONTROLLER ---
            if target_speed == 0.0:
                target_val = 0.0
                integral = 0.0  # Reset windup when stopped
                prev_error = 0.0
            else:
                # Calculate Error
                error = target_speed - speed_mps
                
                # Proportional
                P = Kp * error
                
                # Integral (with anti-windup cap)
                integral += error * dt
                integral = max(min(integral, 2.0), -2.0) # Prevents runaway math
                I = Ki * integral
                
                # Derivative
                derivative = (error - prev_error) / dt if dt > 0 else 0.0
                D = Kd * derivative
                
                # Final PID Output (determines motor power)
                target_val = P + I + D
                prev_error = error

            # Safety clamp to ensure values strictly stay between 0.0 and 0.60 (Max 60% Power)
            target_val = max(0.0, min(0.60, target_val))
                    
            # --- C. APPLY TO MOTORS ---
            if target_val == 0.0:
                left_wheel.mid()
                right_wheel.mid()
            else:
                # Safely cap the left wheel at -1.0 so it doesn't crash the script
                left_val = max(-1.0, -2 * target_val)
                right_wheel.value = target_val
                left_wheel.value = left_val

            # --- D. SENSOR RESET LOGIC ---
            if time.time() - last_time > 1.5 and rpm != 0:
                rpm, rps, speed_mps = 0.0, 0.0, 0.0
                
            # Print to terminal (Now includes RPM and RPS)
            print(f"Time: {elapsed_time:05.1f}s | Tgt: {target_speed:04.2f}m/s | Act: {speed_mps:04.2f}m/s | Pwr: {target_val*100:05.1f}% | RPM: {rpm:05.2f} | RPS: {rps:04.2f}")
            
            # Append to internal lists for plotting
            time_data.append(elapsed_time)
            target_speed_data.append(target_speed)
            speed_data.append(speed_mps)
            rpm_data.append(rpm)
            rps_data.append(rps)
            
            # Write row to CSV and flush to save immediately
            csv_writer.writerow([round(elapsed_time, 3), round(target_speed, 2), round(speed_mps, 2), round(target_val*100, 2), round(rpm, 2), round(rps, 2)])
            csv_file.flush()
            
            # Smaller time step for responsive PID control
            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("\nTest interrupted early by user.")

    finally:
        # ==========================================
        # 5. Safe Teardown & Plotting
        # ==========================================
        print("\nStopping motors and cleaning up...")
        left_wheel.mid()
        right_wheel.mid()
        time.sleep(0.5) 
        left_wheel.detach()
        right_wheel.detach()
        GPIO.cleanup()
        
        print("Generating plot...")
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
        
        ax1.plot(time_data, rps_data, color='tab:green', linewidth=2)
        ax1.set_ylabel('RPS')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_title('Wheel Metrics Over Time (PID Control)')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        time_data_mins = [t / 60.0 for t in time_data]
        ax2.plot(time_data_mins, rpm_data, color='tab:red', linewidth=2)
        ax2.set_ylabel('RPM')
        ax2.set_xlabel('Time (minutes)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Plotting BOTH Target Speed and Actual Speed for visual PID tuning
        ax3.plot(time_data, target_speed_data, color='tab:orange', linewidth=2, linestyle='--', label='Target Speed')
        ax3.plot(time_data, speed_data, color='tab:blue', linewidth=2, label='Actual Speed')
        ax3.set_ylabel('Speed (m/s)')
        ax3.set_xlabel('Time (seconds)')
        ax3.legend(loc='lower right')
        ax3.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(plot_filename, dpi=300)
        
        print(f"Success! CSV saved to: {csv_filename}")
        print(f"Success! Plot saved to: {plot_filename}")
