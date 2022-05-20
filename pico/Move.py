from time import sleep

from micropyGPS import MicropyGPS
import pump
import getTempv318


old_temp = getTempv318.getTemp()

my_gps = MicropyGPS()
print(my_gps.latitude)

def move():
    sleep(2)
    new_temp = getTempv318.getTemp()
    if (new_temp>old_temp):
        pump.pumpRunAB()
    else:
        pump.pumpRunCD()