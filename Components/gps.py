import time
from datetime import datetime 
import serial
from micropyGPS import MicropyGPS

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

# Clear the serial buffer
ser.readline()

i = 0
while 1:
    my_sentence = ser.readline().decode("utf-8")
    #print(str(i))
    #print(my_sentence)
    parse_sentence(my_sentence)
    print(f'[{datetime.now()}] Satellites in view/ Fix type/ use: {my_gps.satellites_in_view}, {my_gps.fix_type}, {my_gps.satellites_used}')
    print(f'Latitude: {my_gps.latitude}, Longitude: {my_gps.longitude}, Altitude: {my_gps.altitude}, Course Degree: {my_gps.course}')
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
