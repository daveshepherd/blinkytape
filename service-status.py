from __future__ import division
import traceback
import time
import math
import random
from BlinkyTape import BlinkyTape
import requests
import logging
import threading
import Queue

q = Queue.Queue()

logging.basicConfig(level=logging.INFO,format='(%(threadName)-10s) %(message)s',)

RED = 1
GREEN = 2

def queryService(url):
    r = requests.get(url, allow_redirects=False)
    if r.status_code == 200:
        logging.warn('.')
        return GREEN
    else:
        logging.warn('Retrying: %s - %s', url, r.status_code)
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            return GREEN
        else:
            logging.error('%s - %s', url, r.status_code)
            return RED

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

def worker():
    logging.info('Starting thread')
    while True:
        logging.info('Starting to query services')
        try:
            q.put(getStatus())
        except:
            traceback.print_exc()
        logging.info('Finished querying services')
        time.sleep(30)

def display():
    logging.info('Starting thread')
    bb = BlinkyTape('/dev/ttyACM0')
    leds = []
    red_leds = 0
    while True:
        try:
            logging.info('Updating display')
            if not q.empty():
                status = q.get()
                red_count = status.count(RED)
                green_count = status.count(GREEN)

                red_ratio = red_count/(red_count + green_count)
                red_leds = int(math.ceil(red_ratio * 60))
                logging.info('Status has been updated, number of red lights: %s', red_leds)

            else:
                logging.info('Status has not been updated')

            logging.info('Populate leds list')
            x = 0
            for i in range(red_leds):
                leds.append([255,0,0])
                x = x + 1
            for i in range(x,60):
                leds.append([0,random.randint(20,255),0])

            for i in range(0,60):
                random.shuffle(leds)
                bb.send_list(leds)
                time.sleep(0.5)

        except:
            traceback.print_exc()

w = threading.Thread(name='worker', target=worker)
d = threading.Thread(name='display', target=display)
logging.debug('Starting threads')
w.start()
d.start()
logging.debug('Threads started')