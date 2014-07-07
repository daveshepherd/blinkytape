import requests
import json
import time
from BlinkyTape import BlinkyTape

bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!
RGB_OFFSET = 17

def getTemperature():
	r = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3544?res=hourly&key=35d53d57-9aa0-45de-9772-0871f0ceffda")
	data = json.loads(r.text)

	periods = data['SiteRep']['DV']['Location']['Period']
	latestPeriod = periods[len(periods) - 1]

	lastSampleDate = latestPeriod['value']
	reports = latestPeriod['Rep']
	lastSampleHour = len(reports) - 1
	currentTemperature = reports[lastSampleHour]['T']
	print "%s %s:00 UTC %s C" % (lastSampleDate, lastSampleHour, currentTemperature)

	return int(float(currentTemperature))

def increasingColourOffset(offset):
		return offset * RGB_OFFSET

def decreasingColourOffset(offset):
		return 255 - increasingColourOffset(offset)


def convertTemperatureToRgb(temperature):
	if (temperature <= -20):
		return [0,0,255]
	elif (temperature <= -5):
		# -20 < t <= -5
		g = increasingColourOffset(temperature + 20)
		return [0,g,255]
	elif (temperature <= 10):
		# -5 < t <= 10
		b = decreasingColourOffset(temperature + 5)
		return [0,255,b]
	elif (temperature <= 25):
		# 10 < t <= 25
		r = increasingColourOffset(temperature - 10)
		return [r,255,0]
	elif (temperature <= 40):
		# 25 < t <= 40
		g = decreasingColourOffset(temperature - 25)
		return [255,g,0]
	else:
		# 40 < t
		return [255,0,0]	

	return [0,0,0]

bb.displayColor(0,0,0)

while True:
	currentTemperature = getTemperature()
	pixelCount = currentTemperature + 20
	print pixelCount if pixelCount > 0 else 0
	colour = convertTemperatureToRgb(currentTemperature)
	print colour

	for i in range(pixelCount):
		colour = convertTemperatureToRgb(i-20)
		bb.sendPixel(colour[0],colour[1],colour[2])
	for i in range(pixelCount,60):
		bb.sendPixel(0,0,0)

	bb.show()
	time.sleep(300)