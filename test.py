# test basic GPIO functions

panServoPin           = 18
tiltServoPin          = 27
laser              = 17
buzzer             = 22





import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(laser, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(laser, False)
GPIO.output(buzzer, False)


GPIO.setup(tiltServoPin, GPIO.OUT)
GPIO.setup(panServoPin, GPIO.OUT)



#test laser pin:
#GPIO.output(laser, True)
#time.sleep(10)
#GPIO.cleanup()




#test buzzer pin:
#GPIO.output(buzzer, True)
#time.sleep(1)
#GPIO.cleanup()


#converts angle parameters to PWM:




#test  servos:
panServo = GPIO.PWM(panServoPin, 50)
panServo.start(2.5)
tiltServo = GPIO.PWM(tiltServoPin, 50)
tiltServo.start(2.5)
try:
    while True:
        panServo.ChangeDutyCycle(5)
        tiltServo.ChangeDutyCycle(5)
        time.sleep(.5)
        panServo.ChangeDutyCycle(16)
        tiltServo.ChangeDutyCycle(16)
        time.sleep(.5)
except KeyboardInterrupt:
    panServo.stop
    tiltServo.stop
    GPIO.cleanup()        



