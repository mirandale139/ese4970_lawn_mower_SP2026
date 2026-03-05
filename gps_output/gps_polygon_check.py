import time
import serial
import math
import csv
from micropyGPS import MicropyGPS

# ----------------------------
# SERIAL PORT SETUP
# ----------------------------

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

gps = MicropyGPS()

# ----------------------------
# LOAD POLYGON FROM CSV
# ----------------------------

polygon = []

with open("/home/gle/ESE4970/gps_output/gps_boundary.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        polygon.append((lat, lon))

print("Polygon loaded with", len(polygon), "points")

# ----------------------------
# CONVERT GPS FORMAT
# ----------------------------

def to_decimal(coord):
    deg, minutes, hemi = coord
    if hemi is None:
        return None

    decimal = deg + minutes / 60.0

    if hemi in ('S','W'):
        decimal *= -1

    return decimal

# ----------------------------
# PARSE GPS SENTENCE
# ----------------------------

def parse_sentence(sentence):
    for char in sentence:
        gps.update(char)

# ----------------------------
# ANGLE BETWEEN VECTORS
# ----------------------------

def angle_between(v1, v2):

    dot = v1[0]*v2[0] + v1[1]*v2[1]

    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if mag1 == 0 or mag2 == 0:
        return 0

    cos_angle = dot/(mag1*mag2)

    cos_angle = max(-1, min(1, cos_angle))

    return math.acos(cos_angle)

# ----------------------------
# POINT IN POLYGON TEST
# ----------------------------

def is_inside_polygon(robot_lat, robot_lon, polygon):

    total_angle = 0
    n = len(polygon)

    for i in range(n):

        p1 = polygon[i]
        p2 = polygon[(i+1) % n]

        v1 = (p1[0] - robot_lat, p1[1] - robot_lon)
        v2 = (p2[0] - robot_lat, p2[1] - robot_lon)

        angle = angle_between(v1, v2)

        cross = v1[0]*v2[1] - v1[1]*v2[0]

        if cross < 0:
            angle = -angle

        total_angle += angle

    if abs(total_angle) > math.pi:
        return True
    else:
        return False

# ----------------------------
# MAIN LOOP
# ----------------------------

print("Starting GPS fence monitor...")

while True:

    sentence = ser.readline().decode("utf-8", errors="ignore")

    parse_sentence(sentence)

    if gps.fix_type >= 2:

        lat = to_decimal(gps.latitude)
        lon = to_decimal(gps.longitude)

        if lat and lon:

            inside = is_inside_polygon(lat, lon, polygon)

            print("Current Position:", lat, lon)

            if inside:
                print("🟢 INSIDE POLYGON\n")
            else:
                print("🔴 OUTSIDE POLYGON\n")

    time.sleep(1)
