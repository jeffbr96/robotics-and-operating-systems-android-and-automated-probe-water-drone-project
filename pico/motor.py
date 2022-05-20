import machine
import time

pin = machine.Pin(2, machine.Pin.OUT)
pwm = machine.PWM(pin)
pwm.freq(50)

while True:
    pwm.duty(51)
    time.sleep(1)
    for d in range(52,103):
        pwm.duty(d)
        time.sleep(0.2)
    time.sleep(1)