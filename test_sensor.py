#!/usr/bin/python

import time, sys, signal, atexit, mraa, thread, threading, os
import pyupm_grove as grove

myIRProximity = mraa.Aio(5)             #GP2Y0A on Analog pin 5

AREF = 5.0
SAMPLES_PER_QUERY = 1024
flag = 1
while 1:
#    Distancevalue = float(myIRProximity.read())*AREF/SAMPLES_PER_QUERY 
    Distancevalue = myIRProximity.read()
    print(str(Distancevalue))
    time.sleep(1.5)
