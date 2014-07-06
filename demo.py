from BlinkyTape import BlinkyTape
from time import sleep


bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!

shortBreak = 0.05
longBreak = 0.5
offColour = [0,0,0]
red = [254,0,0]
green = [0,254,0]
blue = [0,0,254]
orange = [254,140,0]
white = [254,254,254]
flashColour = blue
colorList=[offColour for i in range(60)]

def setColour(colour1, colour2, colour3, colour4, colour5, colour6):
	colorList[0:9] = [colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1,colour1]
	colorList[10:19] = [colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2,colour2]
	colorList[20:29] = [colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3,colour3]
	colorList[30:39] = [colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4,colour4]
	colorList[40:49] = [colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5,colour5]
	colorList[50:59] = [colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6,colour6]

def firstOn():
	setColour(flashColour, offColour, offColour, offColour, flashColour, offColour)
	bb.send_list(colorList)

def secondOn():
	setColour(offColour, flashColour, offColour, offColour, offColour, flashColour)
	bb.send_list(colorList)

def off():
	setColour(offColour, offColour, offColour, offColour, offColour, offColour)
	bb.send_list(colorList)

def ambulance():

	for x in range(6):
		firstOn()
		sleep(shortBreak)
		off()
		sleep(shortBreak)

	for x in range(6):
		secondOn()
		sleep(shortBreak)
		off()
		sleep(shortBreak)

while True:
	ambulance()

#		knightrider()