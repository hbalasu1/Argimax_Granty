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
temp = grove.GroveTemp(0) 				#grove temperature on A0 
myMoisture = upmMoisture.GroveMoisture(1) 		#Moisture sensor on A1
light = grove.GroveLight(2) 				#Light sensor on A2
myUVSensor = upmUV.GUVAS12D(3) 				#UV sensor on A3
stepperX = mylib.StepMotor(2, 3) 			#StepMotorY object on pins 2 (dir) and 3 (step)
stepperY = mylib.StepMotor(4, 5)			#StepMotorX object on pins 4 (dir) and 5 (step)
waterpump = mraa.Gpio(10) 				#Water pump's Relay on GPIO 10
waterpump.dir(mraa.DIR_OUT)
waterpump.write(0)
gServo = servo.ES08A(6)                			#Servo object using D6
gServo.setAngle(50)
switchY = mraa.Gpio(7)    				#SwitchY for GPIO 7
switchY.dir(mraa.DIR_IN)
switchX = mraa.Gpio(8)					#SwitchX for GPIO 8
switchX.dir(mraa.DIR_IN)
EnableStepper = mraa.Gpio(9)				#StepperMotor Enable on GPIO 6
EnableStepper.dir(mraa.DIR_OUT)
EnableStepper.write(1)
button = grove.GroveButton(0)  				#Digital Button on D0   -> ## button.value()

		
# Variable Def
AREF = 5.0
SAMPLES_PER_QUERY = 1024
flag = 1

## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This function lets you run code on exit, including functions from myUVSensor
def exitHandler():
	waterpump.write(0)
	EnableStepper.write(1)
	print "Exiting"
	sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)
	
# Main Function start here
while (flag):
        # Test all 5 Sensors
        '''
	UVvalue = myUVSensor.value(AREF, SAMPLES_PER_QUERY) #Voltage value (higher means more UV)
	Lightvalue = light.value()  # in lux
	Distancevalue = float(myIRProximity.read())*AREF/SAMPLES_PER_QUERY  #Distance in Voltage (higher mean closer)
	Soilvalue = myMoisture.value() # 0-300 Dry, 300-600 Most, <600 Wet
    	Tempvalue = temp.value()  # Celsius
	
	print "Test all the 5 SENSORS :"
	print "1. UV Sensor : 		%d V" % UVvalue
	print "2. Light Sensor : 	%d Lux" % Lightvalue
	print "3. Distance Sensor : 	%f V" % Distancevalue
	print "4. Moisture Sensor : 	%d " % Soilvalue
	print "5. Temperature Sensor :  %d Celsius" % Tempvalue
	
	sensors = [Lightvalue, Distancevalue, Soilvalue, Tempvalue]
	sences = all(value!=0 for value in sensors)
	if (sences): print "All sensors work greate"
	else: print " Somes of the sensor(s) not working "
	
	# Test input value for switch(s) and restart button
	print "Test Input Value, Switch(s) and button"
	print "1. Switch X : %d " % switchX.read()
	print "2. Switch Y : %d " % switchY.read()
	print "3. Button R : %d " % button.value()
        '''
	# Test Stepper Motor (going to initial stages)
	print "Testing Stepper Motor ... "
	print "going to initial stages until switch 0"
	EnableStepper.write(0)
	stepperX.setSpeed(150)
        stepperY.setSpeed(150)
        stepperX.stepForward(1700)
        time.sleep(0.5)
        stepperY.stepBackward(2100)
        time.sleep(0.5)
        stepperX.stepBackward(1200)
        time.sleep(0.3)
        stepperY.stepForward(300)
        time.sleep(1)
        gServo.setAngle(100)
        time.sleep(2)
        waterpump.write(0)   #1
        time.sleep(1.2)
        waterpump.write(0)
        gServo.setAngle(50)
        time.sleep(1)
        stepperY.stepForward(1500)
        time.sleep(0.3)
        stepperX.stepForward(900)
        time.sleep(1)
        gServo.setAngle(100)
        time.sleep(2)
        waterpump.write(0)   #1
        time.sleep(1.2)
        waterpump.write(0)
        gServo.setAngle(50)
        time.sleep(3)
        stepperX.stepForward(300)
        time.sleep(1)
        stepperY.stepBackward(1800)
        EnableStepper.write(1)
        '''
        print "Moving Stepper Motor X"
	while (switchX.read()):
	        stepperX.stepForward(100)
	        time.sleep(0.3)
    
        print "Moving Stepper Motor Y"
	stepperY.setSpeed(150)
        while (switchY.read()):
	        stepperY.stepBackward(100)
	        time.sleep(0.3)
		
	time.sleep(1)
	stepperX.stepBackward(900) 
    	time.sleep(1)
    	stepperY.stepForward(900)
	print "End Stepper Motor Test"
	EnableStepper.write(1)
	
	# Test Water Pump relay 
	print "Activate water pump's Relay"
	waterpump.write(1)
	time.sleep(5)
	waterpump.write(0)
        time.sleep(2)
	print "End Water pump's relay Test, Should hear the sound"
	
	# Test Servo Z-axis position
	print "Test Servo motor function "
        print "Servo z-axis should be down"
	gServo.setAngle(100)
	time.sleep(3.5)
	print "Servo z-axis should be up"
	gServo.setAngle(50)
	time.sleep(1)
        print "Finish all Test :) "
        '''
	flag = 0

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
