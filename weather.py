import requests
import json
import time
from BlinkyTape import BlinkyTape

bb = BlinkyTape('/dev/ttyACM0') #least on Mac OS X, this is the port to use!
RGB_OFFSET = 25

def getTemperature():
	try:
		r = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3544?res=hourly&key=35d53d57-9aa0-45de-9772-0871f0ceffda")
		data = json.loads(r.text)
		print data

		periods = data['SiteRep']['DV']['Location']['Period']
		latestPeriod = periods[len(periods) - 1]

		lastSampleDate = latestPeriod['value']
		reports = latestPeriod['Rep']
		lastSampleHour = len(reports) - 1
		currentTemperature = reports[lastSampleHour]['T']
		print "%s %s:00 UTC %s C" % (lastSampleDate, lastSampleHour, currentTemperature)

		return int(float(currentTemperature))
	except:
		print "Unexpected error:", sys.exc_info()[0]

def increasingColourOffset(offset):
		return offset * RGB_OFFSET

def decreasingColourOffset(offset):
		return 255 - increasingColourOffset(offset)

#20 10 0 10 20 30 40
def convertTemperatureToRgb(temperature):
	if (temperature <= -20):
		return [0,0,255]
	elif (temperature <= -10):
		# -20 < t <= -5
		g = increasingColourOffset(temperature + 20)
		return [0,g,255]
	elif (temperature <= 0):
		# -5 < t <= 10
		b = decreasingColourOffset(temperature + 10)
		return [0,255,b]
	elif (temperature <= 10):
		# 10 < t <= 25
		r = increasingColourOffset(temperature )
		return [r,255,0]
	elif (temperature <= 20):
		# 25 < t <= 40
		g = decreasingColourOffset(temperature - 10)
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
	time.sleep(1800)