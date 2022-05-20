from machine import Pin, PWM
import time
import random
from time import sleep
import getTemp
import machine

###
# setting up the pumps
###

#find out the pumps that are stronger and invert the pins on the ones that arent. 

INA1 = Pin(13, Pin.OUT)
INA2 = Pin(12, Pin.OUT)

INB1 = Pin(9, Pin.OUT)
INB2 = Pin(10, Pin.OUT)

INC1 = Pin(7, Pin.OUT)
INC2 = Pin(6, Pin.OUT)

IND1 = Pin(20, Pin.OUT)
IND2 = Pin(19, Pin.OUT)

speedA = PWM(Pin(15))
speedA.freq(1000)
speedB = PWM(Pin(11))
speedB.freq(1000)
speedC = PWM(Pin(8))
speedC.freq(1000)
speedD = PWM(Pin(18))
speedD.freq(1000)

###
# User utility functions for accessing the pumps
###
    
def pumpStop():
    #stop all pumps
    pumpStopA()
    pumpStopB()
    pumpStopC()
    pumpStopD()
    
def pumpStopA():
    INA1.low()  
    INA2.low()
    
def pumpStopB():
    INB1.low()  
    INB2.low()
    
def pumpStopC():
    INC1.low()  
    INC2.low()
    
def pumpStopD():
    IND1.low()  
    IND2.low()
    
def pumpRunA():
    speedA.duty_u16(129000)
    INA2.high()  #spin forward
    INA1.low()
    
def pumpRunB():
    speedB.duty_u16(129000)
    INB1.high()  #spin forward
    INB2.low()

def pumpRunC():
    speedC.duty_u16(129000)
    INC1.high()  #spin forward
    INC2.low()

def pumpRunD():
    speedD.duty_u16(129000)
    IND2.high()  #spin forward
    IND1.low()

def pumpRunAB():
    pumpRunA()
    pumpRunB()
    
def pumpRunAC():
    pumpRunA()
    pumpRunC()
    
def pumpRunBD():
    pumpRunB()
    pumpRunD()
    
def pumpRunCD():
    pumpRunC()
    pumpRunD()


def seekCold(flag):
    
    uart = machine.UART(0, 115200)

    print('in seekcold 1 ' + str(flag))
    while flag:
        s = uart.read()
        if (s != None):
            s = s.decode()
            print (s)
            
        if s == 'stop':
            print('in seekcold 3 ' + s)
            pumpStop()
            flag = not flag
            s = None
            print(flag)
            
            
        
        t1 = getTemp.getT1() #pump A
        t2 = getTemp.getT2()
        
        if (t1 < t2):
            pumpRunD()
            
        if (t2 < t1):
            pumpRunA()
            
        num = random.randint(0,1)
        
        if num == 0:
            pumpRunC()
        
        elif num == 1:
            pumpRunB()
            
        sleep(5)
        pumpStop()
        
# pumpRunA()
# pumpRunB()
# pumpRunC()
# pumpRunD()
sleep(5)
pumpStop()
#seekCold(True)