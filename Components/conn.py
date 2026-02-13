import serial
print ("read a \\n terminated line from serial TX/RX on GPIO")
with serial.Serial('/dev/serial0', 115200, timeout = 2) as ser:
  print(ser.name ) 
  ser.close()
  ser.open()
  while True:
    line = ser.readline()   # read a '\n' terminated line
    if len(line)>0:
      print(line)
