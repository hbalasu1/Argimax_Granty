#!/usr/bin/python

# Author: HARRY CHAND <hari.chand.balasubramaiam@intel.com>
# Copyright (c) 2014 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time, sys, signal, atexit, mraa, thread, threading, os
import pyupm_grove as grove
import pyupm_guvas12d as upmUV
import pyupm_grovemoisture as upmMoisture
import pyupm_stepmotor as mylib
import pyupm_servo as servo
from multiprocessing import Process

# IO Def
myIRProximity = mraa.Aio(5)  				#GP2Y0A on Analog pin 5
temp = grove.GroveTemp(0) 					#grove temperature on A0 
myMoisture = upmMoisture.GroveMoisture(1) 	#Moisture sensor on A1
light = grove.GroveLight(2) 				#Light sensor on A2
myUVSensor = upmUV.GUVAS12D(3) 				#UV sensor on A3
stepperX = mylib.StepMotor(2, 3) 			#StepMotorY object on pins 2 (dir) and 3 (step)
stepperY = mylib.StepMotor(4, 5)			#StepMotorX object on pins 4 (dir) and 5 (step)
waterpump = mraa.Gpio(10) 					#Water pump's Relay on GPIO 10
waterpump.dir(mraa.DIR_OUT)
waterpump.write(0)
gServo = servo.ES08A(6)                		#Servo object using D6
gServo.setAngle(50)
switchY = mraa.Gpio(7)    					#SwitchY for GPIO 7
switchY.dir(mraa.DIR_IN)
switchX = mraa.Gpio(8)						#SwitchX for GPIO 8
switchX.dir(mraa.DIR_IN)
EnableStepperX = mraa.Gpio(9)				#StepperMotorX Enable on GPIO 9
EnableStepperX.dir(mraa.DIR_OUT)
EnableStepperX.write(1)
EnableStepperY = mraa.Gpio(11)				#StepperMotorY Enable on GPIO 11
EnableStepperY.dir(mraa.DIR_OUT)
EnableStepperY.write(1)
button = grove.GroveButton(0)  				#Digital Button on D0   -> ## button.value()

		
# Variable Def
AREF = 5.0
SAMPLES_PER_QUERY = 1024
flag = 1

# Defined all 5 Sensors
UVvalue = myUVSensor.value(AREF, SAMPLES_PER_QUERY) 				#Voltage value (higher means more UV)
Lightvalue = light.value()  										# in lux
Distancevalue = float(myIRProximity.read())*AREF/SAMPLES_PER_QUERY  #Distance in Voltage (higher mean closer)
Soilvalue = myMoisture.value() 										# 0-300 Dry, 300-600 Most, <600 Wet
Tempvalue = temp.value()  											# Celsius

# Defined Motors
stepperX.setSpeed(150)
stepperY.setSpeed(150)

## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This function lets you run code on exit, including functions from myUVSensor
def exitHandler():
	cleanup_stop_thread()
	gc.collect()
	waterpump.write(0)
	EnableStepperX.write(1)
	EnableStepperY.write(1)
	#sensor.terminate()
	#restart.terminate()
	#Mx.terminate()
	#My.terminate()
	print "Exiting"
	sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)
def init_MotorX():
	if (switchX.read()):
		stepperX.stepForward(3000)
		time.sleep(0.3)
	return
	
def init_MotorY():
	if (switchY.read()):
		stepperY.stepBackward(3000)
		time.sleep(0.3)
	return
	
def Restart_Program():
	while (button.value() == 1):
		cleanup_stop_thread()
        	gc.collect()
		waterpump.write(0)
		EnableStepperX.write(1)
		EnableStepperY.write(1)
		#sensor.terminate()
		#restart.terminate()
		#Mx.terminate()
		#My.terminate()
		os.execv(sys.executable, sys.executable + sys.argv) #os.execv(sys.executable, ['python'] + sys.argv)
	return
	
def initial():
	print "Reset to initial stages ..... "
	# Test input value for switch(s) and restart button
	# Test Stepper Motor (going to initial stages)
	Mx = Process(target = init_MotorX)
	My = Process(target = init_MotorY)
	EnableStepperX.write(0)
	EnableStepperY.write(0)
	Mx.start()
	My.start()
	while (switchX.read() | switchY.read()):
		if (switchX.read()==0): Mx.terminate()
		if (switchY.read()==0): My.terminate()
	EnableStepperX.write(1)
	EnableStepperY.write(1)
	# Turn OFF water pump relay
	waterpump.write(0)
	# Servo z-axis should be up
	gServo.setAngle(50)
	return
	
def MoveToPot(pot):
	print "Moving to Pot %d " %(pot)
	posX = 200; posY = 200
	EnableStepperX.write(0)
	EnableStepperY.write(0)
	if (pot == 1): stepperX.stepBackward(posX); stepperY.stepForward(posY); 
	elif (pot == 2): stepperX.stepBackward(posX+100); stepperY.stepForward(posY+100); 
	elif (pot == 3): stepperX.stepBackward(posX+200); stepperY.stepForward(posY+200); 
	elif (pot == 4): stepperX.stepBackward(posX+300); stepperY.stepForward(posY+300); 
	elif (pot == 5): stepperX.stepBackward(posX+400); stepperY.stepForward(posY+400); 
	elif (pot == 6): stepperX.stepBackward(posX+500); stepperY.stepForward(posY+500); 
	elif (pot == 7): stepperX.stepBackward(posX+600); stepperY.stepForward(posY+600); 
	elif (pot == 8): stepperX.stepBackward(posX+700); stepperY.stepForward(posY+700); 
	elif (pot == 9): stepperX.stepBackward(posX+800); stepperY.stepForward(posY+800); 
	else: print "Invalid operation for Pot Position"; 
	EnableStepperX.write(1)
	EnableStepperY.write(1)
	time.sleep(1)
	return 
	
def PlantMoist(pot):
	print "Check Soil Moisture Pot %d "%(pot)
	if (Distancevalue < 0.9): 
		print "Pot detected !"
		gServo.setAngle(100) 
		time.sleep(1.5)
		
		if (Soilvalue < 300):
			print "Soil value is %d , Need Watering"%(Soilvalue) 
			waterpump.write(1)
			time.sleep(1.3)
			waterpump.write(0)
			time.sleep(1)
			print "Done watering on pot %d"%(pot)
		else: print "Soil in pot %d is already Moisture"%(pot)
	else: print "Pot %d detected"%(pot)		
	gServo.setAngle(50)
	time.sleep(1)
	return 
	
def GetSensorsValue():
	while (1):
		print "Test all the 5 SENSORS :"
		print "1. UV Sensor : 		%d V" % UVvalue
		print "2. Light Sensor : 	%d Lux" % Lightvalue
		print "3. Distance Sensor : 	%f V" % Distancevalue
		print "4. Moisture Sensor : 	%d " % Soilvalue
		print "5. Temperature Sensor :  %d Celsius" % Tempvalue
	return 

# Global Definition
restart = Process(target = Restart_Program) #Go into Initial Stages
sensor = Process(target = GetSensorsValue) #Go into Initial Stages

if __name__ == '__main__':
	while (flag):
		restart.start()
		# Add calling camera modules
		#sensor.start()
		initial()
		for x in range(1,10):
			MoveToPot(x)
			PlantMoist(x)

		flag = 0

	del [light, temp, button, gServo] 
	cleanup_stop_thread()
        gc.collect() 
	#sensor.terminate()
	#restart.terminate()
	#Mx.terminate()
	#My.terminate()

# Information:
## Soil moisture Values (approximate):
# 0-300,   sensor in air or dry soil
# 300-600, sensor in humid soil
# 600+,    sensor in wet soil or submerged in water

## Infrared Proximity Sensor 
# The higher the voltage (closer to AREF) the closer the object is.
# NOTE: The measured voltage will probably not exceed 3.3 volts.
# Every second, print the averaged voltage value
# (averaged over 20 samples).
