#!/usr/bin/python

import time, sys, signal, atexit, mraa, thread, threading, os
import pyupm_servo as servo

gServo = servo.ES08A(6)                		#Servo object using D6
'''
if (sys.argv==50 | sys.argv==100): 
'''
gServo.setAngle(50)
'''	
if (gServo.setAngle==50): print "Set 50, Servo is UP"
	else: print "Set 100, Servo is Down"
else : print "Wrong Arguiment, Please set 50 got UP and 100 for Down"
'''
print "The END"
