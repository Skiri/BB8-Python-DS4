# SpheroBB8-python
**Sphero's BB8 droid** 
*The droid you've been looking for.*

Now even better with a python API library!

Use "sudo hcitool lescan" to find BB8's MAC address 
input it at "`deviceAddress =`" (line 244) in the Sphero class in BB8_driver.py

**

***Included Scripts:***

**
**BB8Test.py**
A simple program that connects to BB8 and flashes the internal RGB LED red to green to blue. You can take it a step further and add `bb8.roll` commands to make him move using the API. 

**BB8joyDrive.py**
*requires PyGame library* 

Allow you to drive BB8 with a joystick/gamepad.
Shows on screen feedback of analog stick as well as speed and heading
Currently setup for a DualShock 4.

	#Dualshock 4 key codes:
	#get_button(0) - Square
	#get_button(1) - X
	#get_button(2) - O
	#get_button(3) - Triangle
	#get_button(4) - L1
	#get_button(5) - R1
	#get_button(6) - L2
	#get_button(7) - R2

> Adapted the sphero driver library from:
> https://github.com/mmwise/sphero_ros/tree/groovy-devel/sphero_driver/src/sphero_driver
> 
> Used the bluetooth 'stuff' from:
> https://gist.github.com/ali1234/5e5758d9c591090291d6


# BB8-Python-DS4
