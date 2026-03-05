import time
from datetime import datetime
import serial
from micropyGPS import MicropyGPS
import os

filename = "/home/gle/ESE4970/gps_output/gps_boundary.csv"

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

my_gps = MicropyGPS()

# Create file if not exists
if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("corner_id,latitude,longitude\n")

# Convert to decimal degrees
def to_decimal(coord):
    deg, minutes, hemi = coord
    if hemi is None:
        return None
    decimal = deg + minutes / 60.0
    if hemi in ('S', 'W'):
        decimal *= -1
    return decimal

def parse_sentence(sentence):
    for char in sentence:
        my_gps.update(char)

import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def collect_average(duration=20):

    wait_for_fix()

    print(f"📡 Collecting GPS data for {duration} seconds...")

    samples = []
    start_time = time.time()

    while time.time() - start_time < duration:

        sentence = ser.readline().decode("utf-8", errors="ignore")
        parse_sentence(sentence)

        # ONLY USE 3D FIX
        if my_gps.fix_type >= 2:

            lat = to_decimal(my_gps.latitude)
            lon = to_decimal(my_gps.longitude)

            if lat is not None and lon is not None:
                samples.append((lat, lon))

    if len(samples) < 5:
        print("❌ Not enough samples.")
        return None, None

    # median
    lats = sorted([s[0] for s in samples])
    lons = sorted([s[1] for s in samples])

    median_lat = lats[len(lats)//2]
    median_lon = lons[len(lons)//2]

    filtered = []

    for lat, lon in samples:
        dist = haversine(lat, lon, median_lat, median_lon)

        if dist < 15:
            filtered.append((lat, lon))

    if len(filtered) < 3:
        print("⚠ Too many outliers removed.")
        return None, None

    #avg_lat = sum(p[0] for p in filtered) / len(filtered)
    #avg_lon = sum(p[1] for p in filtered) / len(filtered)

    filtered.sort()
    avg_lat = filtered[len(filtered)//2][0]
    avg_lon = filtered[len(filtered)//2][1]
    print(f"✅ Used {len(filtered)} filtered samples")
    print(f"Average Position: {avg_lat}, {avg_lon}")

    return avg_lat, avg_lon

def wait_for_fix():

    stable_count = 0

    while stable_count < 5:

        sentence = ser.readline().decode("utf-8", errors="ignore")
        parse_sentence(sentence)

        if my_gps.fix_type >= 2 and my_gps.satellites_in_use >= 4:
            stable_count += 1
        else:
            stable_count = 0

    print("✅ GPS stabilized")
# MAIN LOOP
corner_id = 1

print("🚀 GPS Boundary Collector Started")
print("Type 'yes' when standing at a corner.")
print("Type 'quit' to exit.\n")

while True:

    cmd = input("Command: ").strip().lower()

    if cmd == "quit":
        print("Exiting program.")
        break

    if cmd == "yes":
        avg_lat, avg_lon = collect_average(10)

        if avg_lat is not None:
            with open(filename, "a") as f:
                f.write(f"{corner_id},{avg_lat},{avg_lon}\n")

            print(f"📍 Corner {corner_id} saved.\n")
            corner_id += 1
