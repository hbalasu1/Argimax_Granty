import time, sys, signal, atexit, mraa, thread
waterpump = mraa.Gpio(10)
waterpump.dir(mraa.DIR_OUT)

waterpump.write(1)
time.sleep(1.2)
waterpump.write(0)
time.sleep(0.5)

