#!/usr/bin/env python
#
#  Angle Servo Control 
#  Execute with parameter ==> sudo python3 servoCtrl.py <servo GPIO> <servo_angle> 
#  Execute with parameter ==> sudo python3 servoCtrl.py <pan> <servo_angle> <tilt> <servo_angle>
#  MJRoBot.org 01Feb18
# just for testing.
  
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


panServoPin           = 27
tiltServoPin          = 18
laser 				  = 22
buzzer 				  = 17


GPIO.setup(panServoPin, GPIO.OUT)
GPIO.setup(tiltServoPin, GPIO.OUT)
GPIO.setup(laser, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

def setServoAngle(servo, angle):
	assert angle >=30 and angle <= 150
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

if __name__ == '__main__':
	import sys
	for i in range (1, len(sys.argv)):
		if sys.argv[i] == "pan":
			setServoAngle(panServoPin, int(sys.argv[i + 1]))
			
		
		if sys.argv[i] == "tilt":
			setServoAngle(tiltServoPin, int(sys.argv[i + 1]))
			

		if sys.argv[i] == "laser":
			if sys.argv[i + 1] == "on":
				GPIO.output(laser, True)	

			if sys.argv[i + 1] == "off":
				GPIO.output(laser, False)

		if sys.argv[i] == "buzzer":

			if sys.argv[i + 1] == "on":
				GPIO.output(buzzer, True)	

			if sys.argv[i + 1] == "off":
				GPIO.output(buzzer, False)





