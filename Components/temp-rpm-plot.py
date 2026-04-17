import matplotlib.pyplot as plt

# The raw output pasted from your terminal
raw_data = """
Time: 00.0s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 00.5s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 01.0s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 01.5s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 02.0s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 02.5s | Target Power: 00% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 03.0s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 03.5s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 04.0s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 04.5s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 05.0s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 05.5s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 06.0s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 06.5s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 07.0s | Target Power: 15% | RPM: 00.00 | RPS: 0.00 | Speed: 0.00 m/s
Time: 07.5s | Target Power: 15% | RPM: 54.48 | RPS: 0.91 | Speed: 0.96 m/s
Time: 08.0s | Target Power: 15% | RPM: 54.48 | RPS: 0.91 | Speed: 0.96 m/s
Time: 08.5s | Target Power: 15% | RPM: 54.48 | RPS: 0.91 | Speed: 0.96 m/s
Time: 09.0s | Target Power: 15% | RPM: 54.34 | RPS: 0.91 | Speed: 0.95 m/s
Time: 09.5s | Target Power: 15% | RPM: 54.34 | RPS: 0.91 | Speed: 0.95 m/s
Time: 10.0s | Target Power: 15% | RPM: 55.54 | RPS: 0.93 | Speed: 0.97 m/s
Time: 10.5s | Target Power: 15% | RPM: 55.54 | RPS: 0.93 | Speed: 0.97 m/s
Time: 11.0s | Target Power: 15% | RPM: 55.39 | RPS: 0.92 | Speed: 0.97 m/s
Time: 11.5s | Target Power: 15% | RPM: 55.39 | RPS: 0.92 | Speed: 0.97 m/s
Time: 12.0s | Target Power: 15% | RPM: 55.40 | RPS: 0.92 | Speed: 0.97 m/s
Time: 12.5s | Target Power: 15% | RPM: 55.40 | RPS: 0.92 | Speed: 0.97 m/s
Time: 13.0s | Target Power: 15% | RPM: 55.45 | RPS: 0.92 | Speed: 0.97 m/s
Time: 13.5s | Target Power: 15% | RPM: 55.45 | RPS: 0.92 | Speed: 0.97 m/s
Time: 14.0s | Target Power: 15% | RPM: 55.37 | RPS: 0.92 | Speed: 0.97 m/s
Time: 14.5s | Target Power: 15% | RPM: 55.37 | RPS: 0.92 | Speed: 0.97 m/s
Time: 15.0s | Target Power: 15% | RPM: 56.32 | RPS: 0.94 | Speed: 0.99 m/s
Time: 15.5s | Target Power: 15% | RPM: 56.32 | RPS: 0.94 | Speed: 0.99 m/s
Time: 16.0s | Target Power: 15% | RPM: 56.32 | RPS: 0.94 | Speed: 0.99 m/s
Time: 16.5s | Target Power: 15% | RPM: 51.65 | RPS: 0.86 | Speed: 0.91 m/s
Time: 17.0s | Target Power: 15% | RPM: 51.65 | RPS: 0.86 | Speed: 0.91 m/s
Time: 17.5s | Target Power: 15% | RPM: 57.90 | RPS: 0.96 | Speed: 1.02 m/s
Time: 18.0s | Target Power: 25% | RPM: 57.90 | RPS: 0.96 | Speed: 1.02 m/s
Time: 18.5s | Target Power: 25% | RPM: 55.23 | RPS: 0.92 | Speed: 0.97 m/s
Time: 19.0s | Target Power: 25% | RPM: 55.23 | RPS: 0.92 | Speed: 0.97 m/s
Time: 19.5s | Target Power: 25% | RPM: 55.49 | RPS: 0.92 | Speed: 0.97 m/s
Time: 20.0s | Target Power: 25% | RPM: 55.49 | RPS: 0.92 | Speed: 0.97 m/s
Time: 20.5s | Target Power: 25% | RPM: 56.27 | RPS: 0.94 | Speed: 0.99 m/s
Time: 21.0s | Target Power: 25% | RPM: 56.27 | RPS: 0.94 | Speed: 0.99 m/s
Time: 21.5s | Target Power: 25% | RPM: 55.04 | RPS: 0.92 | Speed: 0.97 m/s
Time: 22.0s | Target Power: 25% | RPM: 55.04 | RPS: 0.92 | Speed: 0.97 m/s
Time: 22.5s | Target Power: 25% | RPM: 55.04 | RPS: 0.92 | Speed: 0.97 m/s
Time: 23.0s | Target Power: 25% | RPM: 54.90 | RPS: 0.92 | Speed: 0.96 m/s
Time: 23.5s | Target Power: 25% | RPM: 54.90 | RPS: 0.92 | Speed: 0.96 m/s
Time: 24.0s | Target Power: 25% | RPM: 54.08 | RPS: 0.90 | Speed: 0.95 m/s
Time: 24.5s | Target Power: 25% | RPM: 54.08 | RPS: 0.90 | Speed: 0.95 m/s
Time: 25.0s | Target Power: 25% | RPM: 51.32 | RPS: 0.86 | Speed: 0.90 m/s
Time: 25.5s | Target Power: 25% | RPM: 51.32 | RPS: 0.86 | Speed: 0.90 m/s
Time: 26.0s | Target Power: 25% | RPM: 55.78 | RPS: 0.93 | Speed: 0.98 m/s
Time: 26.5s | Target Power: 25% | RPM: 55.78 | RPS: 0.93 | Speed: 0.98 m/s
Time: 27.0s | Target Power: 25% | RPM: 55.78 | RPS: 0.93 | Speed: 0.98 m/s
Time: 27.5s | Target Power: 25% | RPM: 55.53 | RPS: 0.93 | Speed: 0.97 m/s
Time: 28.0s | Target Power: 25% | RPM: 55.53 | RPS: 0.93 | Speed: 0.97 m/s
Time: 28.5s | Target Power: 25% | RPM: 54.60 | RPS: 0.91 | Speed: 0.96 m/s
Time: 29.0s | Target Power: 25% | RPM: 54.60 | RPS: 0.91 | Speed: 0.96 m/s
Time: 29.5s | Target Power: 25% | RPM: 54.34 | RPS: 0.91 | Speed: 0.95 m/s
Time: 30.0s | Target Power: 25% | RPM: 54.34 | RPS: 0.91 | Speed: 0.95 m/s
Time: 30.5s | Target Power: 25% | RPM: 55.27 | RPS: 0.92 | Speed: 0.97 m/s
Time: 31.0s | Target Power: 25% | RPM: 55.27 | RPS: 0.92 | Speed: 0.97 m/s
Time: 31.5s | Target Power: 25% | RPM: 55.60 | RPS: 0.93 | Speed: 0.98 m/s
Time: 32.0s | Target Power: 25% | RPM: 55.60 | RPS: 0.93 | Speed: 0.98 m/s
Time: 32.5s | Target Power: 25% | RPM: 57.99 | RPS: 0.97 | Speed: 1.02 m/s
Time: 33.0s | Target Power: 35% | RPM: 57.99 | RPS: 0.97 | Speed: 1.02 m/s
Time: 33.5s | Target Power: 35% | RPM: 56.02 | RPS: 0.93 | Speed: 0.98 m/s
Time: 34.0s | Target Power: 35% | RPM: 56.02 | RPS: 0.93 | Speed: 0.98 m/s
Time: 34.5s | Target Power: 35% | RPM: 62.36 | RPS: 1.04 | Speed: 1.09 m/s
Time: 35.0s | Target Power: 35% | RPM: 62.36 | RPS: 1.04 | Speed: 1.09 m/s
Time: 35.5s | Target Power: 35% | RPM: 83.03 | RPS: 1.38 | Speed: 1.46 m/s
Time: 36.0s | Target Power: 35% | RPM: 83.24 | RPS: 1.39 | Speed: 1.46 m/s
Time: 36.5s | Target Power: 35% | RPM: 83.24 | RPS: 1.39 | Speed: 1.46 m/s
Time: 37.0s | Target Power: 35% | RPM: 83.22 | RPS: 1.39 | Speed: 1.46 m/s
Time: 37.5s | Target Power: 35% | RPM: 83.39 | RPS: 1.39 | Speed: 1.46 m/s
Time: 38.0s | Target Power: 35% | RPM: 83.39 | RPS: 1.39 | Speed: 1.46 m/s
Time: 38.5s | Target Power: 35% | RPM: 83.38 | RPS: 1.39 | Speed: 1.46 m/s
Time: 39.0s | Target Power: 35% | RPM: 83.46 | RPS: 1.39 | Speed: 1.47 m/s
Time: 39.5s | Target Power: 35% | RPM: 83.35 | RPS: 1.39 | Speed: 1.46 m/s
Time: 40.0s | Target Power: 35% | RPM: 83.35 | RPS: 1.39 | Speed: 1.46 m/s
Time: 40.5s | Target Power: 35% | RPM: 83.25 | RPS: 1.39 | Speed: 1.46 m/s
Time: 41.0s | Target Power: 35% | RPM: 82.94 | RPS: 1.38 | Speed: 1.46 m/s
Time: 41.5s | Target Power: 35% | RPM: 82.94 | RPS: 1.38 | Speed: 1.46 m/s
Time: 42.0s | Target Power: 35% | RPM: 83.41 | RPS: 1.39 | Speed: 1.46 m/s
Time: 42.5s | Target Power: 35% | RPM: 83.04 | RPS: 1.38 | Speed: 1.46 m/s
Time: 43.0s | Target Power: 35% | RPM: 83.04 | RPS: 1.38 | Speed: 1.46 m/s
Time: 43.5s | Target Power: 35% | RPM: 83.19 | RPS: 1.39 | Speed: 1.46 m/s
Time: 44.0s | Target Power: 35% | RPM: 83.35 | RPS: 1.39 | Speed: 1.46 m/s
Time: 44.5s | Target Power: 35% | RPM: 83.35 | RPS: 1.39 | Speed: 1.46 m/s
Time: 45.0s | Target Power: 35% | RPM: 83.62 | RPS: 1.39 | Speed: 1.47 m/s
Time: 45.5s | Target Power: 35% | RPM: 83.45 | RPS: 1.39 | Speed: 1.47 m/s
Time: 46.0s | Target Power: 35% | RPM: 83.60 | RPS: 1.39 | Speed: 1.47 m/s
Time: 46.5s | Target Power: 35% | RPM: 83.60 | RPS: 1.39 | Speed: 1.47 m/s
Time: 47.0s | Target Power: 35% | RPM: 83.53 | RPS: 1.39 | Speed: 1.47 m/s
Time: 47.5s | Target Power: 35% | RPM: 83.47 | RPS: 1.39 | Speed: 1.47 m/s
Time: 48.0s | Target Power: 45% | RPM: 83.47 | RPS: 1.39 | Speed: 1.47 m/s
Time: 48.5s | Target Power: 45% | RPM: 83.60 | RPS: 1.39 | Speed: 1.47 m/s
Time: 49.0s | Target Power: 45% | RPM: 83.62 | RPS: 1.39 | Speed: 1.47 m/s
Time: 49.5s | Target Power: 45% | RPM: 83.62 | RPS: 1.39 | Speed: 1.47 m/s
Time: 50.1s | Target Power: 45% | RPM: 83.65 | RPS: 1.39 | Speed: 1.47 m/s
Time: 50.6s | Target Power: 45% | RPM: 83.65 | RPS: 1.39 | Speed: 1.47 m/s
Time: 51.1s | Target Power: 45% | RPM: 83.56 | RPS: 1.39 | Speed: 1.47 m/s
Time: 51.6s | Target Power: 45% | RPM: 83.56 | RPS: 1.39 | Speed: 1.47 m/s
Time: 52.1s | Target Power: 45% | RPM: 83.62 | RPS: 1.39 | Speed: 1.47 m/s
Time: 52.6s | Target Power: 45% | RPM: 83.60 | RPS: 1.39 | Speed: 1.47 m/s
Time: 53.1s | Target Power: 45% | RPM: 83.60 | RPS: 1.39 | Speed: 1.47 m/s
Time: 53.6s | Target Power: 45% | RPM: 83.43 | RPS: 1.39 | Speed: 1.46 m/s
Time: 54.1s | Target Power: 45% | RPM: 83.72 | RPS: 1.40 | Speed: 1.47 m/s
Time: 54.6s | Target Power: 45% | RPM: 83.72 | RPS: 1.40 | Speed: 1.47 m/s
Time: 55.1s | Target Power: 45% | RPM: 83.74 | RPS: 1.40 | Speed: 1.47 m/s
Time: 55.6s | Target Power: 45% | RPM: 82.26 | RPS: 1.37 | Speed: 1.44 m/s
Time: 56.1s | Target Power: 45% | RPM: 82.26 | RPS: 1.37 | Speed: 1.44 m/s
Time: 56.6s | Target Power: 45% | RPM: 83.52 | RPS: 1.39 | Speed: 1.47 m/s
Time: 57.1s | Target Power: 45% | RPM: 83.77 | RPS: 1.40 | Speed: 1.47 m/s
Time: 57.6s | Target Power: 45% | RPM: 83.80 | RPS: 1.40 | Speed: 1.47 m/s
Time: 58.1s | Target Power: 45% | RPM: 83.80 | RPS: 1.40 | Speed: 1.47 m/s
Time: 58.6s | Target Power: 45% | RPM: 83.71 | RPS: 1.40 | Speed: 1.47 m/s
Time: 59.1s | Target Power: 45% | RPM: 83.82 | RPS: 1.40 | Speed: 1.47 m/s
Time: 59.6s | Target Power: 45% | RPM: 83.82 | RPS: 1.40 | Speed: 1.47 m/s
Time: 60.1s | Target Power: 45% | RPM: 83.74 | RPS: 1.40 | Speed: 1.47 m/s
Time: 60.6s | Target Power: 45% | RPM: 83.91 | RPS: 1.40 | Speed: 1.47 m/s
Time: 61.1s | Target Power: 45% | RPM: 83.91 | RPS: 1.40 | Speed: 1.47 m/s
Time: 61.6s | Target Power: 45% | RPM: 84.06 | RPS: 1.40 | Speed: 1.48 m/s
Time: 62.1s | Target Power: 45% | RPM: 84.16 | RPS: 1.40 | Speed: 1.48 m/s
Time: 62.6s | Target Power: 45% | RPM: 84.09 | RPS: 1.40 | Speed: 1.48 m/s
"""

time_data, rpm_data, rps_data, speed_data = [], [], [], []

# Parse the text block
for line in raw_data.strip().split('\n'):
    parts = [p.strip() for p in line.split('|')]
    if len(parts) == 5:
        time_data.append(float(parts[0].replace('Time:', '').replace('s', '')))
        rpm_data.append(float(parts[2].replace('RPM:', '')))
        rps_data.append(float(parts[3].replace('RPS:', '')))
        speed_data.append(float(parts[4].replace('Speed:', '').replace('m/s', '')))

# Generate Plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

ax1.plot(time_data, rps_data, color='tab:green', linewidth=2)
ax1.set_ylabel('RPS')
ax1.set_xlabel('Time (seconds)')
ax1.set_title('Wheel Metrics Over Time (Recovered Data)')
ax1.grid(True, linestyle='--', alpha=0.7)

time_data_mins = [t / 60.0 for t in time_data]
ax2.plot(time_data_mins, rpm_data, color='tab:red', linewidth=2)
ax2.set_ylabel('RPM')
ax2.set_xlabel('Time (minutes)')
ax2.grid(True, linestyle='--', alpha=0.7)

ax3.plot(time_data, speed_data, color='tab:blue', linewidth=2)
ax3.set_ylabel('Speed (m/s)')
ax3.set_xlabel('Time (seconds)')
ax3.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("recovered_wheel_metrics.png", dpi=300)
print("Saved recovered_wheel_metrics.png to your current directory!")
