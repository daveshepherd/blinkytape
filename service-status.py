from __future__ import division
from BlinkyTape import BlinkyTape
import time
import logging
import math
import random
import requests
import threading
import time
import traceback

logging.basicConfig(level=logging.INFO,format='(%(threadName)-10s) %(levelname)-8s %(message)s',)

TEST = False
FAILURE = 1
SUCCESS = 2

c = threading.Condition()
statuses = { "initial": SUCCESS }

def queryService(url):
    r = requests.get(url, allow_redirects=False)
    if r.status_code == 200:
        return SUCCESS
    else:
        logging.warn('Retrying: %s - %s', url, r.status_code)
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            return SUCCESS
        else:
            logging.error('%s - %s', url, r.status_code)
            return FAILURE

def getUrlsForService(service):
    defaultUrlStatuses = {}

    healthUrl = None
    for link in service['links']:
        if link['_id'] == 'health':
            healthUrl = link['url']
            break

    if not healthUrl:
        for link in service['links']:
            if link['_id'] == 'ping':
                healthUrl = link['url']
                break

    for environment in service['environments']:
        if 'baseUrl' in environment:
            defaultUrlStatuses[environment['baseUrl'] + healthUrl] = SUCCESS
    return defaultUrlStatuses

def getDefaultStatuses():
    r = requests.get('https://apps.wealthwizards.io/service-registry/v1/service')
    urlStatuses = {}
    for service in r.json():
        urlStatuses.update(getUrlsForService(service))
    return urlStatuses

def getStatuses(urlStatuses):
    for key in urlStatuses:
		urlStatuses[key] = queryService(key)
    return urlStatuses

def calculateRedLeds(statuses):
    failureCount = sum(1 for x in statuses.values() if x == FAILURE)
    successCount = sum(1 for x in statuses.values() if x == SUCCESS)
    red_ratio = failureCount/(failureCount + successCount)
    red_leds = int(math.ceil(red_ratio * 60))
    return red_leds

def getLedColourList(red_led_count):
    x = 0
    leds = []
    for i in range(red_led_count):
        leds.append([255,0,0])
        x = x + 1
    tail_length = 5
    for i in range(x,60):
        if (red_led_count > 0 and i < x + tail_length):
            tail_count = i-x+1
            shade_of_red = int(math.ceil((tail_length - tail_count + 1) * 64 / (tail_length + 1)))
            leds.append([shade_of_red,0,0])
        else:
            leds.append([0,25,0])
    return leds

def worker():
    global statuses
    logging.info('Starting thread')
    while True:
        logging.info('Starting to query services')
        try:
            defaultStatuses = getDefaultStatuses()

            outOfDateUrls = list(set(statuses.keys()) - set(defaultStatuses.keys()))
            for key in outOfDateUrls:
                del statuses[key]

            newUrls = list(set(defaultStatuses.keys()) - set(statuses.keys()))
            for key in newUrls:
                statuses[key] = defaultStatuses[key]

            getStatuses(statuses)
        except:
            traceback.print_exc()
        logging.info('Finished querying services')

def display():
    current_red_led_count=0
    leds = getLedColourList(current_red_led_count)

    if not TEST:
        bb = BlinkyTape('/dev/ttyACM0')

    logging.info('Starting thread')
    while True:
        red_led_count = calculateRedLeds(statuses)

        # do stuff
        if (current_red_led_count != red_led_count):
            current_red_led_count = red_led_count
            logging.info('Change to number of red lights: %s', current_red_led_count)
            logging.debug('statuses: %s', statuses)
            leds = getLedColourList(current_red_led_count)
        else:
            animate(leds)
        logging.debug(leds)
        if not TEST:
            bb.send_list(leds)
        time.sleep(0.1)

def animate(leds):
    rotate(leds,-1)

def rotate(lst,x):
    copy = list(lst)
    for i in range(len(lst)):
        if x<0:
            lst[i+x] = copy[i]
        else:
            lst[i] = copy[i-x]

w = threading.Thread(name='worker', target=worker)
d = threading.Thread(name='display', target=display)
logging.debug('Starting threads')
w.start()
d.start()
logging.debug('Threads started')