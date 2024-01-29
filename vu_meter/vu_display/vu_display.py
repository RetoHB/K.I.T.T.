#!/usr/bin/python

from .Adafruit_I2C import Adafruit_I2C
from .MCP23017 import MCP23017

import time

GPIOA = 0x12 # register for GPIO port A
GPIOB = 0x13 # register for GPIO port B

mcp1 = MCP23017(address = 0x20, num_gpios = 16) # setup first MCP device
mcp2 = MCP23017(address = 0x21, num_gpios = 16) # setup second MCP device

def setup_vu_meter():
	for pin in range(16):
		mcp1.pinMode(pin, mcp1.OUTPUT) # set mode on all pins to output
		mcp2.pinMode(pin, mcp2.OUTPUT)

def disp_amp(value): # display amplitude for values 0 to 10
	if value in range(11):
		set1A = 0x00 # reset all output values to 0
		set1B = 0x00
		set2A = 0x00
		set2B = 0x00

		for i in range(min(value,8)): # for values smaller or equal than 8,
			set1B |= 1 << i       # set corresponding number of bits on center LED bar

		if value >= 9:                # if value is 9 or higher
			for i in range(min(value-8,2)):
				set1A |= 1 << i # set corresponding number of bits on outer LEDs on center LED bar

		if value >= 4:                # if value is 4 or higher
			for i in range(min(value-3,7)):
				set2A |= 1 << i # set corresponding number of bits on outer LED bars
				set2B = set2A

		mcp1.i2c.write8(GPIOA, set1A) # write set bit patterns to MCP devices
		mcp1.i2c.write8(GPIOB, set1B)
		mcp2.i2c.write8(GPIOA, set2A)
		mcp2.i2c.write8(GPIOB, set2B)

#try:
#	setup_vu_meter()
#	while (True):
#		for value in range(11):
#			disp_amp(value)
#			time.sleep(0.1)
#		for value in range(9):
#			disp_amp(9-value)
#			time.sleep(0.1)

#except KeyboardInterrupt:
#	print ("\n Keyboard interrupt!")
#finally:
#	disp_amp(0)

#	print("Powered down")

