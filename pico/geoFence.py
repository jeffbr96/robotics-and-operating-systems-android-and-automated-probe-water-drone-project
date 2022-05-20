import GPS as gps
import math
import pump
import time
import machine

    
def setFence():
    latBoundUp = 0.0
    latBoundDown = 0.0
    longBoundUp = 0.0
    longBoundDown = 0.0
    
    a, b, c = gps.getLat()
    d, e, f = gps.getLong()
    if b > 0.0:
        latBoundUp = b + 0.001
        latBoundDown = b - 0.001
    else:
        print('latitude not found')
    if e != 0.0:
        longBoundUp = e + 0.01
        longBoundDown = e - 0.01
    else:
        print('longitude not found')
    return (latBoundUp, latBoundDown, longBoundUp, longBoundDown)

def geoFence(x):
    
    uart = machine.UART(0, 115200)
    s = uart.read()
    uart.write('txt stop to stop' +'\r\n')
    if(s != None):
        s = s.decode()
        if (s == 'stop'):
            uart.write('geo fence stoped!' +'\r\n')
            return 'Stoped'
    a, b, c, d = x
    
    if math.isclose(a, 0.0) | math.isclose(b, 0.0) | math.isclose(c, 0.0) | math.isclose(d, 0.0):
        uart.write('sorry fence not established' +'\r\n')
        return 'sorry fence not established'
    
    comp = gps.getCompass()
    
    e = gps.getLat()[1]
    print(str(e) + ' ' + str(a) + ' ' + str(b))
    
    f = gps.getLong()[1]
    print(str(f) + ' ' + str(c) + ' ' + str(d))
    
    with open('geoFence.txt', 'a') as f:
                    f.write('Current compass: ' + comp +'\n' +
                            'upper latitude boundary: ' + str(a) + '\n' +
                            'current latitude: ' + str(e) + '\n' +
                            'lower latitude boundary: ' + str(b) + '\n' +
                            'upper longitude boundary: ' + str(c) + '\n' +
                            'current longitude: ' + str(gps.getLong()[1]) + '\n' +
                            'lower longitude boundary: ' + str(d) + '\n')
    
    if e > a: 
        if comp.find('N') != -1:
            while gps.getCompass().find('N') != -1 & abs(gps.getLat()[1] > a):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: N A pump running; latitude over' + '\n')
                pump.pumpRunA()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
        
        elif comp.find('E') != -1:
            while gps.getCompass().find('E') != -1 & abs(gps.getLat()[1] > a):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: E B pump running; latitude over' + '\n')
                pump.pumpRunB()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('S') != -1:
            while gps.getCompass().find('S') != -1 & abs(gps.getLat()[1] > a):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: S C pump running; latitude over' + '\n')
                pump.pumpRunC()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('W') != -1:
            while gps.getCompass().find('W') != -1 & abs(gps.getLat()[1] > a):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: W D pump running; latitude over' + '\n')
                pump.pumpRunD()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
        
    elif e < b:
        if comp.find('N') != -1:
            while gps.getCompass().find('N') != -1 & abs(gps.getLat()[1] < b):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: N A pump running; latitude under' + '\n')
                pump.pumpRunA()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('E') != -1:
            while gps.getCompass().find('E') != -1 & abs(gps.getLat()[1] < b):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: E B pump running; latitude under' + '\n')
                pump.pumpRunB()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('S') != -1:
            while gps.getCompass().find('S') != -1 & abs(gps.getLat()[1] < b):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: S C pump running; latitude under' + '\n')
                pump.pumpRunC()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('W') != -1:
            while gps.getCompass().find('W') != -1 & abs(gps.getLat()[1] < b):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: W D pump running; latitude under' + '\n')
                pump.pumpRunD()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
        
    elif f > c:
        if comp.find('N') != -1:
            while gps.getCompass().find('N') != -1 & abs(gps.getLong()[1] > c):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: N A pump running; longitude over' + '\n')
                pump.pumpRunA()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('E') != -1:
            while gps.getCompass().find('E') != -1 & abs(gps.getLong()[1] > c):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: E B pump running; longitude over' + '\n')
                pump.pumpRunB()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('S') != -1:
            while gps.getCompass().find('S') != -1 & abs(gps.getLong()[1] > c):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: S C pump running; longitude over' + '\n')
                pump.pumpRunC()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('W') != -1:
            while gps.getCompass().find('W') != -1 & abs(gps.getLong()[1] > c):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: W D pump running; longitude over' + '\n')
                pump.pumpRunD()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
        
    elif f < d:
        if comp.find('N') != -1:
            while gps.getCompass().find('N') != -1 & abs(gps.getLong()[1] < d):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: N A pump running; longitude under' + '\n')
                pump.pumpRunA()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('E') != -1:
            while gps.getCompass().find('E') != -1 & abs(gps.getLong()[1] < d):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: E B pump running; longitude under' + '\n')
                pump.pumpRunB()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('S') != -1:
            while gps.getCompass().find('S') != -1 & abs(gps.getLong()[1] < d):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: S C pump running; longitude under' + '\n')
                pump.pumpRunC()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
        elif comp.find('W') != -1:
            while gps.getCompass().find('W') != -1 & abs(gps.getLong()[1] < d):
                with open('geoFence.txt', 'a') as f:
                    f.write('Compass: W D pump running; longitude under' + '\n')
                pump.pumpRunD()
                s = uart.read()
                if(s != None):
                    s = s.decode()
                    if (s == 'stop'):
                        uart.write('geo fence stoped!' +'\r\n')
                        return 'Stoped'
                    
    pump.pumpStop()
#print(geoFence())

def testCompass():
    uart = machine.UART(0, 115200)
    start_time = time.time()
    seconds = 90
    #fence = setFence()
    while True:
        s = uart.read()
        if (s != None):
            s = s.decode()
            print (s)
            
        if s == 'stoptest':
            pumpStop()
            return 'fail'
        
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(str(elapsed_time) + ' ' + str(seconds))
        
        uart.write(str(gps.getCompass()) +' - \r\n')
        
        if elapsed_time > seconds:
            pump.pumpStop()
            break
