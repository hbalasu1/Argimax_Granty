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

import time, sys, signal, atexit
import pyupm_grove as grove
import pyupm_guvas12d as upmUV
import pyupm_grovemoisture as upmMoisture

# Create the light sensor object using AIO pin 0
light = grove.GroveLight(2);
# Instantiate a UV sensor on analog pin A0
myUVSensor = upmUV.GUVAS12D(3);
# Create the temperature sensor object using AIO pin 0
temp = grove.GroveTemp(0)
# Instantiate a Grove Moisture sensor on analog pin A0
myMoisture = upmMoisture.GroveMoisture(1)

# analog voltage, usually 3.3 or 5.0
GUVAS12D_AREF = 5.0;
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

# Read the input and print both the raw value and a rough lux value,
# waiting one second between readings
while 1:
	# Display UV sensor value
	s = ("AREF:  {0}, "
	"Voltage value (higher means more UV): "
	"{1}".format(GUVAS12D_AREF,
	myUVSensor.value(GUVAS12D_AREF, SAMPLES_PER_QUERY)))
	print s
	
	# Display light sensor value
        print light.name() + " raw value is %d" % light.raw_value() + \
        ", which is roughly %d" % light.value() + " lux"
	
	# Display Temperature sensor value
	celsius = temp.value()
        fahrenheit = celsius * 9.0/5.0 + 32.0;
        print "%d degrees Celsius, or %d degrees Fahrenheit" \
        % (celsius, fahrenheit)
	
	# Display soil Moisture value 
	moisture_val = myMoisture.value()
	if (moisture_val >= 0 and moisture_val < 300):
		result = "Dry"
	elif (moisture_val >= 300 and moisture_val < 600):
		result = "Moist"
	else:
		result = "Wet"
	print "Moisture value: {0}, {1}".format(moisture_val, result)
        print "\n"
	time.sleep(2)


del light  # Delete the light sensor object
del temp   # Delete the temperature sensor object


# Information:
# Soil moisture Values (approximate):
# 0-300,   sensor in air or dry soil
# 300-600, sensor in humid soil
# 600+,    sensor in wet soil or submerged in water
