from BlinkyTape import BlinkyTape
from time import sleep


bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

SHORT_WAIT = 0.05
LONG_WAIT = 0.5
COLOUR_OFF = [0,0,0]
COLOUR_RED = [254,0,0]
COLOUR_GREEN = [0,254,0]
COLOUR_BLUE = [0,0,254]
COLOUR_ORANGE = [254,140,0]
COLOUR_WHITE = [254,254,254]
ACTIVE_COLOUR = COLOUR_BLUE
pixels=[COLOUR_OFF for i in range(60)]

def setColour(colour1, colour2, colour3, colour4, colour5, colour6):
	pixels[0:9] = [colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1]
	pixels[10:19] = [colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2]
	pixels[20:29] = [colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3]
	pixels[30:39] = [colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4]
	pixels[40:49] = [colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5]
	pixels[50:59] = [colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6]

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

#		knightrider()