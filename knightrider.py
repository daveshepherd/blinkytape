from BlinkyTape import BlinkyTape
import urllib2
import re
from time import sleep
import random
import math


bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

OFF_COLOUR = [0,0,0]
DISPLAY_COLOUR = [254,0,0]
R_INTERVAL = DISPLAY_COLOUR[0]/15
G_INTERVAL = DISPLAY_COLOUR[1]/15
B_INTERVAL = DISPLAY_COLOUR[2]/15
DISPLAY_LENGTH = 60
UPDATE_INTERVAL = 0.01

pixels=[OFF_COLOUR for i in range(DISPLAY_LENGTH)]

def fadePixel(pixel):
	if pixel[0] != 0:
		pixel[0] = pixel[0] - R_INTERVAL
		if pixel[0] < 0:
			pixel[0] = 0
	if pixel[1] != 0:
		pixel[1] = pixel[1] - G_INTERVAL
		if pixel[1] < 0:
			pixel[1] = 0
	if pixel[2] != 0:
		pixel[2] = pixel[2] - B_INTERVAL
		if pixel[2] < 0:
			pixel[2] = 0


def fadePixels():
	for x in range(len(pixels)):
		fadePixel(pixels[x])

def knightrider():
	for i in range(DISPLAY_LENGTH):
		fadePixels()
		pixels[i] = list(DISPLAY_COLOUR)
		bb.send_list(pixels)
		sleep(UPDATE_INTERVAL)
	for i in reversed(range(DISPLAY_LENGTH)):
		fadePixels()
		pixels[i] = list(DISPLAY_COLOUR)
		bb.send_list(pixels)
		sleep(UPDATE_INTERVAL)


bb.displayColor(0,0,0)
while True:
	knightrider()