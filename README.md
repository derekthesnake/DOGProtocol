# DOGProtocol
Data Over GPIO Protocol - send data over the GPIO ports on a Raspberry Pi. Useful for when UART ports are non-functional, already in use, or otherwise not available.
RPi PINOUT DIAGRAM:

	+	+
	+	+
	    .
	    .
	    .
	dO	+
	tO	+
	+	+
	+	+
	+	dI
	+	tI

d = data
t = timer

O = out
I = in



1) open two shells on the RPi or have two windows ssh'd into the RPi
2) navigate to the directory that DOGProtocol.py is in using `cd`
3) enter the python3 shell in both windows: `python3`
4) enter the following series of imports in both shells:
>>>import RPi.GPIO as GPIO
>>>import DOGProtocol as DOG
5) enter the following command: `GPIO.setmode(GPIO.BCM)`
6) in one shell, call `DOG.receive()`
7) in the other, call `DOG.send(<string to send>)`
8) profit
