import time
import metoffer
from BlinkyTape import BlinkyTape
from datetime import datetime

bb = BlinkyTape('/dev/ttyACM0')
RGB_OFFSET = 25

def getTemperatures():
	print "getTemperatures start"
	api_key = '35d53d57-9aa0-45de-9772-0871f0ceffda'
	M = metoffer.MetOffer(api_key)
	x = M.nearest_loc_forecast(52.2793,-1.5803, metoffer.THREE_HOURLY)
	y = metoffer.parse_val(x)
	print "data retrieved"

	for i in y.data:
		print("{} - {}".format(i["timestamp"][0].strftime("%d %b, %H:%M"), i["Temperature"][0]))

	print "getTemperatures end"
	return y.data

def increasingColourOffset(offset):
		return offset * RGB_OFFSET

def decreasingColourOffset(offset):
		return 255 - increasingColourOffset(offset)

#20 10 0 10 20 30 40
def convertTemperatureToRgb(temperature):
	if (temperature <= -15):
		return [0,0,255]
	elif (temperature <= -5):
		# -20 < t <= -5
		g = increasingColourOffset(temperature + 15)
		return [0,g,255]
	elif (temperature <= 5):
		# -5 < t <= 10
		b = decreasingColourOffset(temperature + 5)
		return [0,255,b]
	elif (temperature <= 15):
		# 10 < t <= 25
		r = increasingColourOffset(temperature - 5)
		return [r,255,0]
	elif (temperature <= 25):
		# 25 < t <= 40
		g = decreasingColourOffset(temperature - 15)
		return [255,g,0]
	else:
		# 40 < t
		return [255,0,0]	

	return [0,0,0]

bb.displayColor(0,0,0)

while True:
	print "start"
	temps = getTemperatures()

	x = 0
	for i in temps:
		if (datetime.utcnow().day != i["timestamp"][0].day or i["timestamp"][0].hour > datetime.utcnow().hour-3):
			colour = convertTemperatureToRgb(i["Temperature"][0])
			bb.sendPixel(colour[0],colour[1],colour[2])
			x = x + 1
	for i in range(x,60):
		bb.sendPixel(0,0,0)

	bb.show()
	time.sleep(1800)