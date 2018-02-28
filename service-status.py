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

FAILURE = 1
SUCCESS = 2

c = threading.Condition()
red_led_count = 0

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
    urls = []

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
            urls.append(environment['baseUrl'] + healthUrl)
    return urls

def getStatus():
    r = requests.get('https://apps.wealthwizards.io/service-registry/v1/service')

    urls = []
    for service in r.json():
        urls = urls + getUrlsForService(service)

    responses = []
    for url in urls:
		responses.append(queryService(url))

    return responses

def calculateRedLeds(statuses):
    failureCount = statuses.count(FAILURE)
    successCount = statuses.count(SUCCESS)
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
    global red_led_count
    logging.info('Starting thread')
    while True:
        logging.info('Starting to query services')
        try:
            statuses = getStatus()
            c.acquire()
            red_led_count = calculateRedLeds(statuses)
            logging.info('Number of red lights: %s', red_led_count)
            c.notify_all()
            c.release()
        except:
            traceback.print_exc()
        logging.info('Finished querying services')

def display():
    global red_led_count
    current_red_led_count=0
    leds = getLedColourList(current_red_led_count)

    bb = BlinkyTape('/dev/ttyACM0')

    logging.info('Starting thread')
    while True:
        c.acquire()
        new_led_count = red_led_count
        c.notify_all()
        c.release()
        # do stuff
        if (current_red_led_count != new_led_count):
            current_red_led_count = red_led_count
            logging.info('Change to number of red lights: %s', current_red_led_count)
            leds = getLedColourList(current_red_led_count)
        else:
            animate(leds)
        logging.debug(leds)
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