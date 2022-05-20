from machine import Pin, PWM, Timer
import utime

MID = 1500000
MIN = 1000000 
MAX = 2000000
led = Pin(25, Pin.OUT)
timer = Timer()

pwm1 = PWM(Pin(15))
pwm1.freq(50)
pwm1.duty_ns(MID)

pwm2 = PWM(Pin(14))
pwm2.freq(50)
pwm2.duty_ns(MID)

pwm3 = PWM(Pin(13 ))
pwm3.freq(50)
pwm3.duty_ns(MID)

def blink(timer):
    led.toggle()

while True:
    pwm1.duty_ns(MIN)
    utime.sleep(1)
    pwm2.duty_ns(MIN)
    utime.sleep(1)
    pwm3.duty_ns(MIN)
    utime.sleep(1)
    
    pwm1.duty_ns(MAX)
    utime.sleep(1)
    pwm2.duty_ns(MAX)
    utime.sleep(1)
    pwm3.duty_ns(MAX)
    utime.sleep(1)
    