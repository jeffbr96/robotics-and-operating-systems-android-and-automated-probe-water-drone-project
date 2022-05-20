from machine import Pin, UART, I2C
from micropyGPS import MicropyGPS

import utime, time

mgps = MicropyGPS()
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

def getGPS():
    x = gpsModule.readline()
    with open('gps.txt', 'a') as f:
        f.write(str(x) + '\n')
    return x

def testGPS():
    while True:
        sgps = str(gpsModule.readline())[2:-1]
        time.sleep(1)
        for x in sgps:
            mgps.update(x)
        print(sgps)
        print(mgps.compass_direction())
        print(mgps.latitude)
        print(mgps.satellite_data_updated())
    
def getLat():
    #gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    for i in range(3):
        sgps = str(gpsModule.readline())[2:-1]
        for x in sgps:
            mgps.update(x)
        time.sleep(1)
    x = mgps.latitude
    with open('gps.txt', 'a') as f:
        f.write(str(x) + '\n')
    return x

def getLong():
    for i in range(3):
        sgps = str(gpsModule.readline())[2:-1]
        for x in sgps:
            mgps.update(x)
        time.sleep(1)
    x = mgps.longitude
    with open('gps.txt', 'a') as f:
        f.write(str(x) + '\n')
    return x

def getUp():
    for i in range(3):
        sgps = str(gpsModule.readline())
        for x in sgps:
            mgps.update(x)
        time.sleep(1)
    return mgps.satellite_data_updated()

def getCompass():
    for i in range(3):
        sgps = str(gpsModule.readline())
        for x in sgps:
            mgps.update(x)
        time.sleep(1)
    x = mgps.compass_direction()
    with open('gps.txt', 'a') as f:
        f.write(str(x) + '\n')
    return mgps.compass_direction()

#testGPS()