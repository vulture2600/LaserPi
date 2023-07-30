
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCamPanTilt.py
#  	Streaming video with Flask based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with PanTilt position Control
#
#   MJRoBot.org 30Jan18

import os
from time import sleep
from flask import Flask, render_template, request, Response

import io
import picamera

# Raspberry Pi camera module (requires picamera package from Miguel Grinberg)
#from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
global laserStatus
global buzzerStatus

panServoAngle = 90
tiltServoAngle = 90
laserStatus = "off"
buzzerStatus = "off"



@app.route('/')
def index():
    """Video streaming home page."""
 
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
    return render_template('index.html', **templateData)


#def gen(camera):
 #   """Video streaming generator function."""
 #   while True:
 #       frame = camera.get_frame()
 #      yield (b'--frame\r\n'
 #              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		panServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + "pan" + " " + str(panServoAngle))
	if servo == 'tilt':
		tiltServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + "tilt" + " " + str(tiltServoAngle))
	
	templateData = {
    	'panServoAngle'	: panServoAngle,
    	'tiltServoAngle': tiltServoAngle,
    	'laserStatus'   : laserStatus,
        'buzzerStatus'	: buzzerStatus
	}
	return render_template('index.html', **templateData)

@app.route("/laser/<status>")
def laserStatusChange (status):
    global laserStatus
    laserStatus = str(status)
    os.system("python3 angleServoCtrl.py " + "laser " + str(laserStatus))
    templateData = {
          'panServoAngle' : panServoAngle,
          'tiltServoAngle': tiltServoAngle,
          'laserStatus'   : laserStatus,
          'buzzerStatus'  : buzzerStatus          
	}
    return render_template('index.html', **templateData)
    
@app.route("/buzzer/<status>")
def buzzerStatusChange (status):
    global buzzerStatus
    buzzerStatus = str(status)
    os.system("python3 angleServoCtrl.py " + "buzzer " + str(buzzerStatus))
    templateData = {
          'panServoAngle' : panServoAngle,
          'tiltServoAngle': tiltServoAngle,
          'laserStatus'   : laserStatus,
          'buzzerStatus'  : buzzerStatus	
	}
    return render_template('index.html', **templateData)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True, threaded=True)

