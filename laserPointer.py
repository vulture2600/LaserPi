#Sammy Door for Raspberry Pi!
#steve.a.mccluskey@gmail.com
#
# pin layout:
# 01) 3.3v
# 02) 5v
# 03) GPIO 2 -> I2C SDA
# 04) 5v
# 05) GPIO 3 -> I2C SCL
# 06) GND
# 07) GPIO 4 -> OneWire Bus
# 08) GPIO14 -> UART TXT
# 09) GND
# 10) GPIO15 -> UART RXD
# 11) GPIO17 -> buzzer
# 12) GPIO18 -> panServo
# 13) GPIO27 -> tiltServo
# 14) GND
# 15) GPIO22 -> laser
# 16) GPIO23 -> 
# 17) 3.3v
# 18) GPIO24 ->
# 19) GPIO10 -> SPI MOSI
# 20) GND
#
# 21) GPIO 9 -> SPI MISO
# 22) GPIO25
# 23) GPIO11 -> SPI SCLK
# 24) GPIO 8 -> SPI CE0
# 25) GND
# 26) GPIO 7 -> SPI CE1
# 27) ID SD  -> I2C BUS6 SDA
# 28) ID SC  -> I2C BUS6 SCL
# 29) GPIO 5
# 30) GND
# 31) GPIO 6
# 32) GPIO12
# 33) GPIO13
# 34) GND
# 35) GPIO19 -> PCM FS
# 36) GPIO16
# 37) GPIO26 -> N.C.
# 38) GPIO20 -> PCM DIN
# 39) GND
# 40) GPIO21 -> PCM DOUT

from   typing import AnyStr
import board
import bitbangio
import busio
import busio2
import RPi.GPIO as GPIO
from   board import *
import digitalio
import time
from   time import sleep
import mb_24x256_512_CP
import asyncio
import pigpio
from   flask import Flask
from   flask import request
from   flask_cors import CORS
import atexit
import threading
import os
import logging



#############################################################
#pin assignment stuff:
panServo           = 18
tiltServo          = 27
laser              = 22
buzzer             = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(laser,    GPIO.OUT)
GPIO.setup(buzzer,   GPIO.OUT)


#servos:
pwm = pigpio.pi()
pwm.set_mode(panServo, pigpio.OUTPUT)
pwm.set_mode(tiltServo, pigpio.OUTPUT)

pwm.set_PWM_frequency(panServo, 0)
pwm.set_PWM_frequency(tiltServo, 0)



###########################################
#webserver stuff:

app = Flask(__name__)
CORS(app)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR) #loggin to console disabled



#converts angle parameters to PWM:
def degreesToPwm(degree):
    return int((degree) * (2000) / (180) + 500)


##############################
#main event loop:
def mainLoop():
    

    while True:
      

######################################
#server code:
@app.route("/lockIn")
def remoteLockin():
    global lockInEnabled
    lockRequest = request.args.get("enable")

    if (lockRequest == "enable"):
        lockInEnabled = True

    elif (lockRequest == "disable"):
        lockInEnabled = False

    returnString = "recieved : " + str(lockRequest) + " command"
    print (returnString)
    return returnString

@app.route("/getStatus")
def getStatusRequest():
    global lockInEnabled
    global doorStatus
    global lockStatus
    statusString = '{"status" : [{"doorState": '
    if (doorState == 1):
        statusString += '1, '
    else:
        statusString += '0, '
    statusString +='"doorStatus": ' 
    if (doorStatus == 1):
        statusString += '1, '
    else:
        statusString += '0, '
    statusString += '"lockStatus": '
    if (lockStatus == 1):
        statusString += '1, '
    else:
        statusString += '0, '
    statusString += '"lockIn": '
    if (lockInEnabled == True):
        statusString += '1, '
    else:
        statusString += '0, '
    statusString += '"timeStamp": '
    statusString += str(time.time())
    statusString += '}]}'
    print(statusString)
    return statusString

################################
#program start:




mainLoopThread = threading.Thread(target = mainLoop)
mainLoopThread.start()



#start server if not already running:
test = os.popen('sudo netstat -lpn | grep :5000')
print(test.read())
if __name__ == "__main__":
    app.run(host='0.0.0.0')