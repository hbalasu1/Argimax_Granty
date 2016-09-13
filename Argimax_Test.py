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

import time, sys, signal, atexit, mraa, thread
import pyupm_grove as grove
import pyupm_guvas12d as upmUV
import pyupm_grovemoisture as upmMoisture
import pyupm_stepmotor as mylib
import pyupm_servo as servo

# IO Def
myIRProximity = mraa.Aio(5)  				#GP2Y0A on Analog pin 5
temp = grove.GroveTemp(0) 					#grove temperature on A0 
myMoisture = upmMoisture.GroveMoisture(1) 	#Moisture sensor on A1
light = grove.GroveLight(2) 				#Light sensor on A2
myUVSensor = upmUV.GUVAS12D(3) 				#UV sensor on A3
stepperX = mylib.StepMotor(2, 3) 			#StepMotorX object on pins 2 (dir) and 3 (step)
stepperY = mylib.StepMotor(4, 5)			#StepMotorY object on pins 4 (dir) and 5 (step)
waterpump = mraa.Gpio(6) 					#Water pump's Relay on GPIO 6 
waterpump.dir(mraa.DIR_OUT)
waterpump.write(0)
gServo = servo.ES08A(6)                		#Servo object using D6
switchX = mraa.Gpio(7)    					#SwitchX for GPIO 7
switchX.dir(mraa.DIR_IN)
switchY = mraa.Gpio(8)						#SwitchY for GPIO 8
switchY.dir(mraa.DIR_IN)
EnableStepper = mraa.Gpio(9)				#StepperMotor Enable on GPIO 9
EnableStepper.dir(mraa.DIR_OUT)
EnableStepper.write(1)
button = grove.GroveButton(0)  				#Digital Button on D0   -> ## button.value()

		
# Variable Def
AREF = 5.0
SAMPLES_PER_QUERY = 1024
looping = TRUE

## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This function lets you run code on exit, including functions from myUVSensor
def exitHandler():
	print "Exiting"
	sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)
	
# Main Function start here
while looping:
	# Test all 5 Sensors
	UVvalue = myUVSensor.value(AREF, SAMPLES_PER_QUERY) #Voltage value (higher means more UV)
	Lightvalue = light.value()  # in lux
	Distancevalue = float(myIRProximity.read())*AREF/SAMPLES_PER_QUERY  #Distance in Voltage (higher mean closer)
	Soilvalue = myMoisture.value() # 0-300 Dry, 300-600 Most, <600 Wet
    	Tempvalue = temp.value()  # Celsius
	
	print "Test all the 5 SENSORS :"
	print "1. UV Sensor : 			%d" % UVvalue
	print "2. Light Sensor : 		%d" % Lightvalue
	print "3. Distance Sensor : 	%d" % Distancevalue
	print "4. Moisture Sensor : 	%d" % Soilvalue
	print "5. Temperature Sensor : 	%d" % Tempvalue
	
	sensors = [Lightvalue, Distancevalue, Soilvalue, Tempvalue]
	sences = all(value!=0 for value in sensors)
	if (sences): print "All sensors work greate"
	else: print " Somes of the sensor(s) not working "
	
	# Test Stepper Motor (going to initial stages)
	print "Testing Stepper Motor ... "
	print "going to initial stages"
	EnableStepper.write(0)
	stepperX.setSpeed(150)
	x_for = x_bac = y_for = y_bac = 1
	while switchX.read() == 1:
		stepperX.stepForward(x_for)
		x_for+=1
		time.sleep(0.3)
        
	stepperY.setSpeed(150)
	while switchX.read() == 1:
		stepperY.stepForward(y_for)
		y_for+=1
		time.sleep(0.3)
		
	time.sleep(1)
	stepperX.stepBackward(200) 
    	time.sleep(1)
    	stepperY.stepBackward(200)
	print "End Stepper Motor Test"
	EnableStepper.write(1)
	
	# Test Water Pump relay 
	print "Activate water pump's Relay"
	waterpump.write(1)
	time.sleep(3)
	waterpump.write(0)
	print "End Water pump's relay Test, Should hear the sound"
	
	# Test Servo Z-axis position
	print "Test Servo motor function "
	gServo.setAngle(0)
	time.sleep(1)
	print "Servo z-axis should be down"
	gServo.setAngle(90)
	time.sleep(1)
	gServo.setAngle(180)
	time.sleep(1)
	print "Servo z-axis should be up"
	gServo.setAngle(90)
	time.sleep(1)
	gServo.setAngle(0)
	time.sleep(1)
	
	# Test input value for switch(s) and restart button
	print "Reading input value ; SwitchX: %d ; SwitchY: %d ; RestartButton: %d ."% (switchX.read(), switchY.read(), button.value()) 
	looping = FALSE

del [light, temp, button, gServo]  


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
