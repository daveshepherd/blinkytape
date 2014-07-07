from BlinkyTape import BlinkyTape
from time import sleep

bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

SHORT_WAIT = 0.05
COLOUR_OFF = [0,0,0]
COLOUR_RED = [254,0,0]
COLOUR_GREEN = [0,254,0]
COLOUR_BLUE = [0,0,254]
COLOUR_ORANGE = [254,100,0]
COLOUR_WHITE = [254,254,254]
ACTIVE_COLOUR = COLOUR_BLUE
pixels=[COLOUR_OFF for i in range(60)]

def setColour(colour1, colour2, colour3, colour4, colour5, colour6):
	for i in range(0,10):
		pixels[i]=colour1
	for i in range(10,20):
		pixels[i]=colour2
	for i in range(20,30):
		pixels[i]=colour3
	for i in range(30,40):
		pixels[i]=colour4
	for i in range(40,50):
		pixels[i]=colour5
	for i in range(50,60):
		pixels[i]=colour6

def firstOn():
	setColour(ACTIVE_COLOUR, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, ACTIVE_COLOUR, COLOUR_OFF)
	bb.send_list(pixels)

def secondOn():
	setColour(COLOUR_OFF, ACTIVE_COLOUR, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, ACTIVE_COLOUR)
	bb.send_list(pixels)

def off():
	setColour(COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF, COLOUR_OFF)
	bb.send_list(pixels)

def ambulance():

	for x in range(6):
		firstOn()
		sleep(SHORT_WAIT)
		off()
		sleep(SHORT_WAIT)

	for x in range(6):
		secondOn()
		sleep(SHORT_WAIT)
		off()
		sleep(SHORT_WAIT)

while True:
	ambulance()
