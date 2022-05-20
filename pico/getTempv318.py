import machine, onewire, ds18x20, time

#ds_pin = machine.Pin(21)
#ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
#print(ds_sensor.read_temp(ds_sensor.scan()[0]))

def getTemp():
    ds_pin = machine.Pin(21)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    temp = 0
    time.sleep_ms(500)
        
    for rom in roms:
        print (rom)
        temp = ds_sensor.read_temp(rom)
        print (temp)
        return temp
getTemp()