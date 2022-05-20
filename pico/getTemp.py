import machine, onewire, ds18x20, time
 
ds_pin = machine.Pin(21)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

def getT1():
    ds_pin = machine.Pin(21)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
     
    roms = ds_sensor.scan()
    #print('Found DS devices: ', roms)
    ds_sensor.convert_temp()
    temp = ds_sensor.read_temp(roms[0])
    time.sleep_ms(750)
    print(temp)
    return temp

def getT2():
    ds_pin = machine.Pin(22)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
     
    roms = ds_sensor.scan()
    #print('Found DS devices: ', roms)
    ds_sensor.convert_temp()
    temp = ds_sensor.read_temp(roms[0])
    time.sleep_ms(750)
    print(temp)
    return temp