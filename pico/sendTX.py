from machine import UART, Pin
import utime,time

SSID='NETGEAR36'
password = 'fuzzypotato890'
ServerIP = '192.168.1.6'
Port = '10000'

uart = UART(0, 115200)

def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
            print(s)
            if(s.find(ack) >= 0):
                return True
    return False

uart.write('+++')
time.sleep(1)
if(uart.any()>0):uart.read()
sendCMD("AT","OK")
sendCMD("AT+CWMODE=3","OK")
sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
sendCMD("AT+CIFSR","OK")
sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000)
sendCMD("AT+CIPMODE=1","OK")
sendCMD("AT+CIPSEND",">")

uart.write('Hello World, I am ready to send data!!!\r\n')
uart.write('ESP8266 TCP Client\r\n')

#uart.write(getLat())

while True:
    s=uart.read()
    if(s != None):
        s=s.decode()
        print(s)

#time.sleep(5)
while True:
    sendCMD("AT+CIPSEND",">")
    uart.write(getLat())

