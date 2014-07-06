from BlinkyTape import BlinkyTape
import urllib2
import re
from time import sleep
import random
import math


bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

def knightrider():
	for x in range(75):
		for y in range(60):
			if x == y:
				bb.sendPixel(255,0,0)
			elif x-1 == y:
				bb.sendPixel(238,0,0)
			elif x-2 == y:
				bb.sendPixel(221,0,0)
			elif x-3 == y:
				bb.sendPixel(204,0,0)
			elif x-4 == y:
				bb.sendPixel(187,0,0)
			elif x-5 == y:
				bb.sendPixel(170,0,0)
			elif x-6 == y:
				bb.sendPixel(153,0,0)
			elif x-7 == y:
				bb.sendPixel(136,0,0)
			elif x-8 == y:
				bb.sendPixel(119,0,0)
			elif x-9 == y:
				bb.sendPixel(102,0,0)
			elif x-10 == y:
				bb.sendPixel(85,0,0)
			elif x-11 == y:
				bb.sendPixel(68,0,0)
			elif x-12 == y:
				bb.sendPixel(51,0,0)
			elif x-13 == y:
				bb.sendPixel(34,0,0)
			elif x-14 == y:
				bb.sendPixel(17,0,0)
			else:
				bb.sendPixel(0,0,0)
		sleep(0.005)
		bb.show()
	for x in reversed(range(75)):
		for y in range(15, 75):
			if x == y:
				bb.sendPixel(255,0,0)
			elif x+1 == y:
				bb.sendPixel(238,0,0)
			elif x+2 == y:
				bb.sendPixel(221,0,0)
			elif x+3 == y:
				bb.sendPixel(204,0,0)
			elif x+4 == y:
				bb.sendPixel(187,0,0)
			elif x+5 == y:
				bb.sendPixel(170,0,0)
			elif x+6 == y:
				bb.sendPixel(153,0,0)
			elif x+7 == y:
				bb.sendPixel(136,0,0)
			elif x+8 == y:
				bb.sendPixel(119,0,0)
			elif x+9 == y:
				bb.sendPixel(102,0,0)
			elif x+10 == y:
				bb.sendPixel(85,0,0)
			elif x+11 == y:
				bb.sendPixel(68,0,0)
			elif x+12 == y:
				bb.sendPixel(51,0,0)
			elif x+13 == y:
				bb.sendPixel(34,0,0)
			elif x+14 == y:
				bb.sendPixel(17,0,0)
			else:
				bb.sendPixel(0,0,0)
		sleep(0.005)
		bb.show()

while True:
	knightrider()