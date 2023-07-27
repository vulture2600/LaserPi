# test basic GPIO functions

panServoPin           = 18
tiltServoPin          = 27
laser              = 17
buzzer             = 22





import RPi.GPIO as GPIO
import pigpio
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
def degreesToPwm(degree):
    return int((degree) * (2000) / (180) + 500)



#test  servos:
#useful duty cycle range seems to be between 3 and 10 duty cycle
panServo = GPIO.PWM(panServoPin, 50)
panServo.start(5)
tiltServo = GPIO.PWM(tiltServoPin, 50)
tiltServo.start(5)
print("start")
time.sleep(5)

try:
    while True:
        panServo.ChangeDutyCycle(3)
        tiltServo.ChangeDutyCycle(3)
        print("duty cycle low range.")
        time.sleep(2)
        panServo.ChangeDutyCycle(10)
        tiltServo.ChangeDutyCycle(10)
        print("cuty cycle high range.")
        time.sleep(2)
except KeyboardInterrupt:

    panServo.stop
    tiltServo.stop
    GPIO.cleanup()        



