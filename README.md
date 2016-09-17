# Argimax_Granty with Intel Edison
Agriculture Robot for plant maintaining

# Example code for python. 
Most of the code are getting from upm library
* [es08a.js] For servo control code
* [gp2y0a.js] For Distance sensor control code
* [grovebutton.js] For grove button read code
* [grovelight.js] for grove light control code
* [grovemoisture.js] for grove moisture sensor code
* [grovetemp.js] for grove temperature sensor code
* [guvas12d.js] for grove UV detection sensor control code
* [stepmotor.js]  for stepper motor control code

# Example code for JavaScript
Most of the code are getting form upm library
* [es08a.py] For servo control code
* [gp2y0a.py] For Distance sensor control code
* [grovebutton.py] For grove button read code
* [grovelight.py] for grove light control code
* [grovemoisture.py] for grove moisture sensor code
* [grovetemp.py] for grove temperature sensor code
* [guvas12d.py] for grove UV detection sensor control code
* [stepmotor.py]  for stepper motor control code
* [th02.py]  for tempterature and humidity sensor control code
* [servo.py]  for servo motor control library
* [sweep.py]  for servo motor to move from 0 to 90 degree

# WebSocket Example
all code are getting from google :) 
Installing python-pip  and tornado
http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html
then 
https://packaging.python.org/installing/

Another example based on asyncio and Autobahn
http://websockets.readthedocs.io/en/stable/intro.html

Another example based on web-ssocket-client (without any .html)
https://pypi.python.org/pypi/websocket-client/


#Pin Connection to Intel Edison :
	Proximity Sensor (Analog 5)
	Grove - Temperature (A0)
	Grove - Moisture Sensor (A1)              
	Grove - Light Sensor (A2)                     
	Grove - UV Sensor (A3)                        
	Grove - Servor (D6)

	Water pump with Relay and V.resistor (GPIO 10)
	Stepper Motor Y  (DIR,2   STP,3)
	Stepper Motor X (DIR,4    STP,5)
	LED  (GPIO ?)
	Camera (USB)
 
	Touch switch X (GPIO 7)
	Touch switch Y (GPIO 8)
	StepperMotor Enable (GPIO 9) [not suing it]
	Restart button   (GPIO  1)  -> to restart the software and motor position
	
	Emergency Button (to cut off 12v Power)
