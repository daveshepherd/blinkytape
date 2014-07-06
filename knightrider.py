from BlinkyTape import BlinkyTape
import urllib2
import re
from time import sleep
import random
import math


bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

OFF_COLOUR = [0,0,0]
RED = [254,0,0]
DISPLAY_LENGTH = 30
UPDATE_INTERVAL = 0.02

pixels=[OFF_COLOUR for i in range(DISPLAY_LENGTH)]

def fadePixel(pixel):
	if pixel[0] != 0:
		pixel[0] = pixel[0] - 17
		if pixel[0] < 0:
			pixel[0] = 0


def fadePixels():
	for x in range(len(pixels)):
		fadePixel(pixels[x])

def knightrider():
	for i in range(DISPLAY_LENGTH):
		fadePixels()
		pixels[i] = list(RED)
		bb.send_list(pixels)
		sleep(UPDATE_INTERVAL)
	for i in reversed(range(DISPLAY_LENGTH)):
		fadePixels()
		pixels[i] = list(RED)
		bb.send_list(pixels)
		sleep(UPDATE_INTERVAL)


bb.displayColor(0,0,0)
while True:
	knightrider()