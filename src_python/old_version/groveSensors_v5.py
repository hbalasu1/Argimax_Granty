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
#import pyupm_gp2y0a as upmGp2y0a
import pyupm_th02

# Create the light sensor object using AIO pin 0
light = grove.GroveLight(2);
# Instantiate a UV sensor on analog pin A0
myUVSensor = upmUV.GUVAS12D(3);
# Instantiate a Grove Moisture sensor on analog pin A0
myMoisture = upmMoisture.GroveMoisture(1)
# Instantiate a GP2Y0A on analog pin A1
myIRProximity = mraa.Aio(0)
#defined THo2 i2c address
th02 = pyupm_th02.TH02(6,0x40)
# Instantiate a StepMotorX object on pins 2 (dir) and 3 (step)
stepperX = mylib.StepMotor(2, 3)
# Instantiate a StepMotorY object on pins 4 (dir) and 5 (step)
stepperY = mylib.StepMotor(4, 5)

# analog voltage, usually 3.3 or 5.0 for GUVAS12D
AREF = 5.0;
SAMPLES_PER_QUERY = 1024;


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


# Function Display UV sensor value
def UVsensor():
	s = ("AREF:  {0}, "
	"Voltage value (higher means more UV): "
	"{1}".format(AREF,
	myUVSensor.value(AREF, SAMPLES_PER_QUERY)))
	print s
	return s;

# Function Display light sensor value
def Lightsensor():
	print light.name() + " raw value is %d" % light.raw_value() + \
        ", which is roughly %d" % light.value() + " lux"
	return light.value();

# Function Display Distance sensor value
def Distancesensor():
	Vproximity = float(myIRProximity.read())*AREF/SAMPLES_PER_QUERY)
	print "Distance in VOltage (higher mean closer) : " + str(Vproximity)
	return Vproximity;

# Function Display soil Moisture value
def Soilsensor():
	moisture_val = myMoisture.value()
	if (moisture_val >= 0 and moisture_val < 300):
		result = "Dry"
	elif (moisture_val >= 300 and moisture_val < 600):
		result = "Moist"
	else:
		result = "Wet"
	print "Moisture value: {0}, {1}".format(moisture_val, result)
	return moisture_val;

# Function Display Temperature and humidity
def TempTH02():
	print "Temperature value is : " + str(th02.getTemperature())
	print "The value of Humidity : " + str(th02.getHumidity ())
	return th02.getTemperature();

# Read the input and print both the raw value and a rough lux value,
# waiting one second between readings
while 1:
	UVvalue = UVsensor()
	Lightvalue = Lightsensor()
	Distancevalue = Distancesensor()
	Soilvalue = Soilsensor()
	Tempvalue = TempTH02()
	
	# Moving Motor to left and right direction
	print "Rotating 1 revolution forward and back at 150 rpm."
	stepper.setSpeed(150)
	stepper.stepForward(200)
	time.sleep(1)
	stepper.stepBackward(200)
	print "End Stepper Motor"
	time.sleep(2)
	
	print UVvalue+" , "+Lightvalue+" , "+Distancevalue+" , "+Soilvalue+" , "+Tempvalue+" ."


del light  # Delete the light sensor object
del temp   # Delete the temperature sensor object
del th02   # Delete the tho2 sensor object


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
