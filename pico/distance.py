import machine, onewire, ds18x20, time

analog1 = machine.ADC(26)
analog2 = machine.ADC(27)
analog3 = machine.ADC(28)
analog4 = machine.ADC(16)

reading = analog1.read_u16()
print("ADC 1: ", reading)
time.sleep(0.1)

def getAnalog1():
    return analog1

def getAnalog2():    
    return analog2

def getAnalog3():    
    return analog3

def getAnalog4():    
    return analog4

