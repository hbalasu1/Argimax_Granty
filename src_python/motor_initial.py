#!/usr/bin/python

import time, sys, signal, atexit, mraa, thread, threading, os
import pyupm_stepmotor as mylib
from multiprocessing import Process

stepperX = mylib.StepMotor(2, 3) 			#StepMotorY object on pins 2 (dir) and 3 (step)
stepperY = mylib.StepMotor(4, 5)			#StepMotorX object on pins 4 (dir) and 5 (step)

EnableStepperX = mraa.Gpio(9)				#StepperMotorX Enable on GPIO 9
EnableStepperX.dir(mraa.DIR_OUT)
EnableStepperX.write(1)
EnableStepperY = mraa.Gpio(11)				#StepperMotorY Enable on GPIO 11
EnableStepperY.dir(mraa.DIR_OUT)
EnableStepperY.write(1)

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
	EnableStepperX.write(1)
	EnableStepperY.write(1)
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
	return

if __name__ == '__main__':
	initial()

	print "Motor Initial Finished"	
