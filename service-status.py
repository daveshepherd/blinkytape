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
from multiprocessing import Process, Queue
from itertools import islice

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

def slave(queue, urls):
    for url in urls:
        queue.put([url, queryService(url)])
    queue.put(None) # add a sentinel value to tell the master we're done

def chunks(data, SIZE=30):
    it = iter(data)
    for i in xrange(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

def getStatuses(urlStatuses):
    queue = Queue()
    num_procs = 0
    procs = []
    for subset in chunks(urlStatuses, 30):
        procs.append(Process(target=slave, args=(queue, subset, )))
        num_procs += 1
    for proc in procs:
        proc.start()

    finished = 0
    while finished < num_procs:
        item = queue.get()
        if item is None:
            finished += 1
        else:
            urlStatuses[item[0]] = item[1]

    for proc in procs:
        proc.join()

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
        time.sleep(120)

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

d = threading.Thread(name='display', target=display)
d.daemon = True
logging.debug('Starting threads')
d.start()
worker()