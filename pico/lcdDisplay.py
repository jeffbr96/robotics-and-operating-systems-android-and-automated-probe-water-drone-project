from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import utime
from time import sleep
import machine

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(26), scl=machine.Pin(27), freq=400000)
utime.sleep_ms(100)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
utime.sleep_ms(100)

# lcd.putchar(chr(247))
# lcd.putstr("jeff" + '\n')
# lcd.putstr("Hardware")
# sleep(10)

# for i in range(10):
#         lcd.backlight_on()
#         sleep(0.2)
#         lcd.backlight_off()
#         sleep(0.2)

def check():
    devices = i2c.scan()
    if len(devices) == 0:
      print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))
    for device in devices:
      print("Hexa address: ",hex(device))

def blink():
    for i in range(3):
            lcd.backlight_on()
            sleep(0.2)
            lcd.backlight_off()
            sleep(0.1)
            
#blink()
