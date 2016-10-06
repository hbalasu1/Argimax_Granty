#!/usr/bin/python

import time, sys, signal, atexit, mraa, thread, threading, os
import pyupm_grove as grove
import pyupm_guvas12d as upmUV
import pyupm_grovemoisture as upmMoisture
import pyupm_stepmotor as mylib
import pyupm_servo as servo
from multiprocessing import Process

# IO Def
myIRProximity = mraa.Aio(5)  			#GP2Y0A on Analog pin 5
temp = grove.GroveTemp(0) 			#grove temperature on A0 
myMoisture = upmMoisture.GroveMoisture(1) 	#Moisture sensor on A1
light = grove.GroveLight(2) 			#Light sensor on A2
myUVSensor = upmUV.GUVAS12D(3) 			#UV sensor on A3
stepperX = mylib.StepMotor(2, 3) 		#StepMotorY object on pins 2 (dir) and 3 (step)
stepperY = mylib.StepMotor(4, 5)		#StepMotorX object on pins 4 (dir) and 5 (step)
waterpump = mraa.Gpio(10) 			#Water pump's Relay on GPIO 10
waterpump.dir(mraa.DIR_OUT)
waterpump.write(0)
gServo = servo.ES08A(6)                		#Servo object using D6
gServo.setAngle(50)
switchY = mraa.Gpio(7)    			#SwitchY for GPIO 7
switchY.dir(mraa.DIR_IN)
switchX = mraa.Gpio(8)				#SwitchX for GPIO 8
switchX.dir(mraa.DIR_IN)
EnableStepperX = mraa.Gpio(9)			#StepperMotorX Enable on GPIO 9
EnableStepperX.dir(mraa.DIR_OUT)
EnableStepperX.write(1)
EnableStepperY = mraa.Gpio(11)			#StepperMotorY Enable on GPIO 11
EnableStepperY.dir(mraa.DIR_OUT)
EnableStepperY.write(1)
button = grove.GroveButton(0)  			#Digital Button on D0   

stepperX.setSpeed(150)
stepperY.setSpeed(150)

while(switchX.read()):
	stepperX.stepForward(200)
	time.sleep(0.3)
	return
