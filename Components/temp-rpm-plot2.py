import matplotlib.pyplot as plt

# The raw output pasted from your terminal
raw_data = """
Arming motors... (Ctrl+C to stop early)
Time: 000.0s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 000.5s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 001.0s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 001.5s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 002.0s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 002.5s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 003.0s | Target Power: 000.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 003.5s | Target Power: 000.6% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 004.0s | Target Power: 001.2% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 004.5s | Target Power: 001.8% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 005.0s | Target Power: 002.4% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 005.5s | Target Power: 003.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 006.0s | Target Power: 003.6% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 006.5s | Target Power: 004.2% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 007.0s | Target Power: 004.8% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 007.5s | Target Power: 005.4% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 008.0s | Target Power: 006.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 008.5s | Target Power: 006.6% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 009.0s | Target Power: 007.2% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 009.5s | Target Power: 007.8% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 010.0s | Target Power: 008.4% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 010.5s | Target Power: 009.0% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 011.0s | Target Power: 009.6% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 011.5s | Target Power: 010.2% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 012.0s | Target Power: 010.8% | RPM: 06.08 | RPS: 0.10 | Speed: 0.11 m/s
Time: 012.5s | Target Power: 011.4% | RPM: 06.08 | RPS: 0.10 | Speed: 0.11 m/s
Time: 013.0s | Target Power: 012.0% | RPM: 06.08 | RPS: 0.10 | Speed: 0.11 m/s
Time: 013.5s | Target Power: 012.6% | RPM: 40.63 | RPS: 0.68 | Speed: 0.71 m/s
Time: 014.0s | Target Power: 013.2% | RPM: 40.63 | RPS: 0.68 | Speed: 0.71 m/s
Time: 014.5s | Target Power: 013.8% | RPM: 40.63 | RPS: 0.68 | Speed: 0.71 m/s
Time: 015.0s | Target Power: 014.4% | RPM: 39.75 | RPS: 0.66 | Speed: 0.70 m/s
Time: 015.5s | Target Power: 015.0% | RPM: 39.75 | RPS: 0.66 | Speed: 0.70 m/s
Time: 016.0s | Target Power: 015.6% | RPM: 39.75 | RPS: 0.66 | Speed: 0.70 m/s
Time: 016.5s | Target Power: 016.2% | RPM: 40.46 | RPS: 0.67 | Speed: 0.71 m/s
Time: 017.0s | Target Power: 016.8% | RPM: 40.46 | RPS: 0.67 | Speed: 0.71 m/s
Time: 017.5s | Target Power: 017.4% | RPM: 40.46 | RPS: 0.67 | Speed: 0.71 m/s
Time: 018.0s | Target Power: 018.0% | RPM: 40.35 | RPS: 0.67 | Speed: 0.71 m/s
Time: 018.5s | Target Power: 018.6% | RPM: 40.35 | RPS: 0.67 | Speed: 0.71 m/s
Time: 019.0s | Target Power: 019.2% | RPM: 40.35 | RPS: 0.67 | Speed: 0.71 m/s
Time: 019.5s | Target Power: 019.8% | RPM: 40.87 | RPS: 0.68 | Speed: 0.72 m/s
Time: 020.0s | Target Power: 020.4% | RPM: 40.87 | RPS: 0.68 | Speed: 0.72 m/s
Time: 020.5s | Target Power: 021.0% | RPM: 40.87 | RPS: 0.68 | Speed: 0.72 m/s
Time: 021.0s | Target Power: 021.6% | RPM: 40.01 | RPS: 0.67 | Speed: 0.70 m/s
Time: 021.5s | Target Power: 022.2% | RPM: 40.01 | RPS: 0.67 | Speed: 0.70 m/s
Time: 022.0s | Target Power: 022.8% | RPM: 40.01 | RPS: 0.67 | Speed: 0.70 m/s
Time: 022.5s | Target Power: 023.4% | RPM: 39.72 | RPS: 0.66 | Speed: 0.70 m/s
Time: 023.0s | Target Power: 024.0% | RPM: 39.72 | RPS: 0.66 | Speed: 0.70 m/s
Time: 023.5s | Target Power: 024.6% | RPM: 39.72 | RPS: 0.66 | Speed: 0.70 m/s
Time: 024.0s | Target Power: 025.2% | RPM: 39.82 | RPS: 0.66 | Speed: 0.70 m/s
Time: 024.5s | Target Power: 025.8% | RPM: 39.82 | RPS: 0.66 | Speed: 0.70 m/s
Time: 025.0s | Target Power: 026.4% | RPM: 39.82 | RPS: 0.66 | Speed: 0.70 m/s
Time: 025.5s | Target Power: 027.0% | RPM: 41.53 | RPS: 0.69 | Speed: 0.73 m/s
Time: 026.0s | Target Power: 027.6% | RPM: 41.53 | RPS: 0.69 | Speed: 0.73 m/s
Time: 026.5s | Target Power: 028.2% | RPM: 41.53 | RPS: 0.69 | Speed: 0.73 m/s
Time: 027.0s | Target Power: 028.8% | RPM: 38.77 | RPS: 0.65 | Speed: 0.68 m/s
Time: 027.5s | Target Power: 029.4% | RPM: 38.77 | RPS: 0.65 | Speed: 0.68 m/s
Time: 028.0s | Target Power: 030.0% | RPM: 38.77 | RPS: 0.65 | Speed: 0.68 m/s
Time: 028.5s | Target Power: 030.6% | RPM: 38.43 | RPS: 0.64 | Speed: 0.67 m/s
Time: 029.0s | Target Power: 031.2% | RPM: 38.43 | RPS: 0.64 | Speed: 0.67 m/s
Time: 029.5s | Target Power: 031.8% | RPM: 73.69 | RPS: 1.23 | Speed: 1.29 m/s
Time: 030.0s | Target Power: 032.4% | RPM: 82.76 | RPS: 1.38 | Speed: 1.45 m/s
Time: 030.5s | Target Power: 033.0% | RPM: 83.20 | RPS: 1.39 | Speed: 1.46 m/s
Time: 031.0s | Target Power: 033.6% | RPM: 83.20 | RPS: 1.39 | Speed: 1.46 m/s
Time: 031.5s | Target Power: 034.2% | RPM: 83.63 | RPS: 1.39 | Speed: 1.47 m/s
Time: 032.0s | Target Power: 034.8% | RPM: 83.77 | RPS: 1.40 | Speed: 1.47 m/s
Time: 032.5s | Target Power: 035.4% | RPM: 83.77 | RPS: 1.40 | Speed: 1.47 m/s
Time: 033.0s | Target Power: 036.0% | RPM: 83.80 | RPS: 1.40 | Speed: 1.47 m/s
Time: 033.5s | Target Power: 036.6% | RPM: 83.42 | RPS: 1.39 | Speed: 1.46 m/s
Time: 034.0s | Target Power: 037.2% | RPM: 83.42 | RPS: 1.39 | Speed: 1.46 m/s
Time: 034.5s | Target Power: 037.9% | RPM: 83.61 | RPS: 1.39 | Speed: 1.47 m/s
Time: 035.0s | Target Power: 038.5% | RPM: 83.61 | RPS: 1.39 | Speed: 1.47 m/s
Time: 035.5s | Target Power: 039.1% | RPM: 83.57 | RPS: 1.39 | Speed: 1.47 m/s
Time: 036.0s | Target Power: 039.7% | RPM: 83.57 | RPS: 1.39 | Speed: 1.47 m/s
Time: 036.5s | Target Power: 040.3% | RPM: 83.77 | RPS: 1.40 | Speed: 1.47 m/s
Time: 037.0s | Target Power: 040.9% | RPM: 83.95 | RPS: 1.40 | Speed: 1.47 m/s
Time: 037.5s | Target Power: 041.5% | RPM: 83.95 | RPS: 1.40 | Speed: 1.47 m/s
Time: 038.0s | Target Power: 042.1% | RPM: 83.05 | RPS: 1.38 | Speed: 1.46 m/s
Time: 038.5s | Target Power: 042.7% | RPM: 83.50 | RPS: 1.39 | Speed: 1.47 m/s
Time: 039.0s | Target Power: 043.3% | RPM: 83.50 | RPS: 1.39 | Speed: 1.47 m/s
Time: 039.5s | Target Power: 043.9% | RPM: 83.79 | RPS: 1.40 | Speed: 1.47 m/s
Time: 040.1s | Target Power: 044.5% | RPM: 83.55 | RPS: 1.39 | Speed: 1.47 m/s
Time: 040.6s | Target Power: 045.1% | RPM: 83.55 | RPS: 1.39 | Speed: 1.47 m/s
Time: 041.1s | Target Power: 045.7% | RPM: 83.55 | RPS: 1.39 | Speed: 1.47 m/s
Time: 041.6s | Target Power: 046.3% | RPM: 83.30 | RPS: 1.39 | Speed: 1.46 m/s
Time: 042.1s | Target Power: 046.9% | RPM: 83.48 | RPS: 1.39 | Speed: 1.47 m/s
Time: 042.6s | Target Power: 047.5% | RPM: 83.48 | RPS: 1.39 | Speed: 1.47 m/s
Time: 043.1s | Target Power: 048.1% | RPM: 83.81 | RPS: 1.40 | Speed: 1.47 m/s
Time: 043.6s | Target Power: 048.7% | RPM: 84.08 | RPS: 1.40 | Speed: 1.48 m/s
Time: 044.1s | Target Power: 049.3% | RPM: 84.08 | RPS: 1.40 | Speed: 1.48 m/s
Time: 044.6s | Target Power: 049.9% | RPM: 84.00 | RPS: 1.40 | Speed: 1.47 m/s
Time: 045.1s | Target Power: 050.5% | RPM: 83.64 | RPS: 1.39 | Speed: 1.47 m/s
Time: 045.6s | Target Power: 051.1% | RPM: 83.64 | RPS: 1.39 | Speed: 1.47 m/s
Time: 046.1s | Target Power: 051.7% | RPM: 83.75 | RPS: 1.40 | Speed: 1.47 m/s
Time: 046.6s | Target Power: 052.3% | RPM: 83.81 | RPS: 1.40 | Speed: 1.47 m/s
Time: 047.1s | Target Power: 052.9% | RPM: 83.61 | RPS: 1.39 | Speed: 1.47 m/s
Time: 047.6s | Target Power: 053.5% | RPM: 83.61 | RPS: 1.39 | Speed: 1.47 m/s
Time: 048.1s | Target Power: 054.1% | RPM: 83.96 | RPS: 1.40 | Speed: 1.47 m/s
Time: 048.6s | Target Power: 054.7% | RPM: 84.10 | RPS: 1.40 | Speed: 1.48 m/s
Time: 049.1s | Target Power: 055.3% | RPM: 84.10 | RPS: 1.40 | Speed: 1.48 m/s
Time: 049.6s | Target Power: 055.9% | RPM: 84.21 | RPS: 1.40 | Speed: 1.48 m/s
Time: 050.1s | Target Power: 056.5% | RPM: 84.18 | RPS: 1.40 | Speed: 1.48 m/s
Time: 050.6s | Target Power: 057.1% | RPM: 84.10 | RPS: 1.40 | Speed: 1.48 m/s
Time: 051.1s | Target Power: 057.7% | RPM: 84.10 | RPS: 1.40 | Speed: 1.48 m/s
Time: 051.6s | Target Power: 058.3% | RPM: 84.02 | RPS: 1.40 | Speed: 1.47 m/s
Time: 052.1s | Target Power: 058.9% | RPM: 83.95 | RPS: 1.40 | Speed: 1.47 m/s
Time: 052.6s | Target Power: 059.5% | RPM: 83.95 | RPS: 1.40 | Speed: 1.47 m/s
Time: 053.1s | Target Power: 060.1% | RPM: 84.18 | RPS: 1.40 | Speed: 1.48 m/s
Time: 053.6s | Target Power: 060.7% | RPM: 69.63 | RPS: 1.16 | Speed: 1.22 m/s
Time: 054.1s | Target Power: 061.3% | RPM: 69.63 | RPS: 1.16 | Speed: 1.22 m/s
Time: 054.6s | Target Power: 061.9% | RPM: 76.68 | RPS: 1.28 | Speed: 1.35 m/s
Time: 055.1s | Target Power: 062.5% | RPM: 76.68 | RPS: 1.28 | Speed: 1.35 m/s
Time: 055.6s | Target Power: 063.1% | RPM: 82.53 | RPS: 1.38 | Speed: 1.45 m/s
Time: 056.1s | Target Power: 063.7% | RPM: 82.49 | RPS: 1.37 | Speed: 1.45 m/s
Time: 056.6s | Target Power: 064.3% | RPM: 82.81 | RPS: 1.38 | Speed: 1.45 m/s
Time: 057.1s | Target Power: 064.9% | RPM: 82.81 | RPS: 1.38 | Speed: 1.45 m/s
Read from remote host 172.27.56.198: Connection reset by peer
Connection to 172.27.56.198 closed.
client_loop: send disconnect: Broken pipe
(base) giangle@Giangs-MacBook-Pro ~ % ssh gle@172.27.56.198
"""

time_data, rpm_data, rps_data, speed_data = [], [], [], []

# Parse the text block
for line in raw_data.strip().split('\n'):
    # Skip any line that doesn't contain valid data (like SSH errors)
    if not line.startswith('Time:'):
        continue
        
    parts = [p.strip() for p in line.split('|')]
    if len(parts) == 5:
        # Extract the numbers, stripping out words and extra characters
        time_val = float(parts[0].replace('Time:', '').replace('s', '').strip())
        rpm_val = float(parts[2].replace('RPM:', '').strip())
        rps_val = float(parts[3].replace('RPS:', '').strip())
        speed_val = float(parts[4].replace('Speed:', '').replace('m/s', '').strip())
        
        time_data.append(time_val)
        rpm_data.append(rpm_val)
        rps_data.append(rps_val)
        speed_data.append(speed_val)

# Generate Plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

# Subplot 1: RPS
ax1.plot(time_data, rps_data, color='tab:green', linewidth=2)
ax1.set_ylabel('RPS')
ax1.set_xlabel('Time (seconds)')
ax1.set_title('Wheel Metrics Over Time (Recovered Smooth Ramp)')
ax1.grid(True, linestyle='--', alpha=0.7)

# Subplot 2: RPM (Converted to minutes)
time_data_mins = [t / 60.0 for t in time_data]
ax2.plot(time_data_mins, rpm_data, color='tab:red', linewidth=2)
ax2.set_ylabel('RPM')
ax2.set_xlabel('Time (minutes)')
ax2.grid(True, linestyle='--', alpha=0.7)

# Subplot 3: Speed
ax3.plot(time_data, speed_data, color='tab:blue', linewidth=2)
ax3.set_ylabel('Speed (m/s)')
ax3.set_xlabel('Time (seconds)')
ax3.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
output_filename = "recovered_smooth_metrics.png"
plt.savefig(output_filename, dpi=300)
print(f"Saved {output_filename} to your current Mac directory!")
