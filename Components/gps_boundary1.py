import time
from datetime import datetime
import serial
from micropyGPS import MicropyGPS
import os
import math

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


def haversine(lat1, lon1, lat2, lon2):

    R = 6371000  # meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi/2)**2 +
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def collect_average(duration=20):

    print(f"\n📡 Collecting GPS data for {duration} seconds...")

    samples = []
    start_time = time.time()

    while time.time() - start_time < duration:

        sentence = ser.readline().decode("utf-8", errors="ignore")
        parse_sentence(sentence)

        if my_gps.fix_type >= 2:

            lat = to_decimal(my_gps.latitude)
            lon = to_decimal(my_gps.longitude)

            if lat and lon:
                samples.append((lat, lon))

    if len(samples) < 5:
        print("❌ Not enough samples.")
        return None, None


    # ---- STEP 1: Find median point ----
    lats = sorted([s[0] for s in samples])
    lons = sorted([s[1] for s in samples])

    median_lat = lats[len(lats)//2]
    median_lon = lons[len(lons)//2]


    # ---- STEP 2: Remove outliers beyond threshold ----
    filtered = []

    for lat, lon in samples:

        dist = haversine(lat, lon, median_lat, median_lon)

        if dist < 15:   # 15 meters threshold
            filtered.append((lat, lon))


    if len(filtered) < 3:
        print("⚠ Too many outliers removed.")
        return None, None


    # ---- STEP 3: Average filtered points ----
    avg_lat = sum([p[0] for p in filtered]) / len(filtered)
    avg_lon = sum([p[1] for p in filtered]) / len(filtered)

    print(f"✅ Used {len(filtered)} filtered samples")
    print(f"Average Position: {avg_lat}, {avg_lon}")

    return avg_lat, avg_lon


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

        avg_lat, avg_lon = collect_average(30)

        if avg_lat is not None:

            with open(filename, "a") as f:
                f.write(f"{corner_id},{avg_lat},{avg_lon}\n")

            print(f"📍 Corner {corner_id} saved.\n")

            corner_id += 1
