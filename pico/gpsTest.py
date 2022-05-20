from micropyGPS import MicropyGPS
from machine import Pin, UART

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

mgps = MicropyGPS()
print(mgps.compass_direction())
print(mgps.satellite_data_updated())