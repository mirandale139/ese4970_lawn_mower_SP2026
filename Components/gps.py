import time
from datetime import datetime 
import serial
from micropyGPS import MicropyGPS
import os

filename = "/home/gle/ESE4970/gps_output/gps_data.csv"

ser = serial.Serial(
        port='/dev/serial0',
        # port='COM3',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)        

def parse_sentence(sentence):        
    for i in range(len(sentence)):
        my_sentence = sentence[i]
        for k in my_sentence:
            my_gps.update(k)
            
    #print('')
    #print(sentence)

#my_gps = MicropyGPS(-5)
#my_sentence = '$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'

my_gps = MicropyGPS()
status = False
last_lat = None
last_lon = None

# Create header only if file doesn't exist
if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("timestamp,latitude,longitude,altitude,fix_type,satellites_in_use,course\n")

# Convert Latitude/Longitude: [degrees, minutes, hemisphere] to Decimals
def to_decimal(coord):
    deg, minutes, hemi = coord
    if hemi is None:
        return None
    decimal = deg + minutes / 60.0
    if hemi in ('S', 'W'):
        decimal *= -1
    return decimal

# Clear the serial buffer
ser.readline()

i = 0
while 1:
    my_sentence = ser.readline().decode("utf-8")
    #print(str(i))
    #print(my_sentence)
    parse_sentence(my_sentence)

    lat = my_gps.latitude
    lon = my_gps.longitude

    # Check if valid fix
    valid_fix = (
        my_gps.fix_type >= 2 and lat[2] is not None and lon[2] is not None)

    if status:
    # 🔍 KEEP EVERYTHING EXACTLY THE SAME
        print("\n{datetime.now()} - Satellites in view/ Fix type/ use:",
          my_gps.satellites_in_view,
          my_gps.fix_type,
          my_gps.satellites_in_use)
        print("Latitude:", lat,
          "Longitude:", lon,
          "Altitude:", my_gps.altitude,
          "Course Degree:", my_gps.course)

    else:
    # 🚀 Only print when GPS actually updates position
        if valid_fix and (lat != last_lat or lon != last_lon):

            print("\n{datetime.now()} - Satellites in view/ Fix type/ use:",
              my_gps.satellites_in_view,
              my_gps.fix_type,
              my_gps.satellites_in_use)
            print("Latitude:", lat,
              "Longitude:", lon,
              "Altitude:", my_gps.altitude,
              "Course Degree:", my_gps.course)

     # SAVE TO CSV-
            lat_dd = to_decimal(lat)
            lon_dd = to_decimal(lon)

            with open(filename, "a") as f:
                f.write("{},{},{},{},{},{},{}\n".format(
                            my_gps.timestamp,
                            lat_dd,
                            lon_dd,
                            my_gps.altitude,
                            my_gps.fix_type,
                            my_gps.satellites_in_use,
                            my_gps.course))

            last_lat = lat
            last_lon = lon
    #print(f'[{datetime.now()}] Satellites in view/ Fix type/ use: {my_gps.satellites_in_view}, {my_gps.fix_type}, {my_gps.satellites_used}')
    #print(f'		Latitude: {my_gps.latitude}, Longitude: {my_gps.longitude}, Altitude: {my_gps.altitude}, Course Degree: {my_gps.course}')
    
    i += 1

print(f'Latitude: {my_gps.latitude}')
print(f'Longitude: {my_gps.longitude}')
print(f'Course: {my_gps.course}')
print(f'Altitude: {my_gps.altitude}')
print(f'Geoid Height: {my_gps.geoid_height}')
print(f'Speed: {my_gps.speed}')
print(f'Compass Direction: {my_gps.compass_direction()}')

print(f'Offset: {my_gps.local_offset}')
print(f'Timestamp: {my_gps.timestamp}')
print(f'Date: {my_gps.date}')

print(f'Satellites in use: {my_gps.satellites_used}')
print(f'Fix type: {my_gps.fix_type}')
print(f'        1=no fix, 2=2D fix, 3=3D fix')

print(f'Check if ind satellite data? {my_gps.satellite_data_updated()}')
print(f'Satellites: {my_gps.satellite_data}')
print(f'Visible Satellites: {my_gps.satellites_visible()}')
