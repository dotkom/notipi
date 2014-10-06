#!/bin/env python2
from wiringpi2 import *
import datetime
import requests
import time
try:
    from settings import API_KEY, NAME
except ImportError:
    raise SystemExit('settings.py not found')


LIGHT_PIN = 12
BUTTON_PIN = 13
LED_PIN = 14

INPUT = 0
OUTPUT = 1

HIGH = 1
LOW = 0

URL = "http://passoa.online.ntnu.no/notiwire/" + NAME + '/'


def main():
    setup()
    counter = 0
    pots = 0
    while True:
        # Light
        if counter >= 0:
            counter = int(1E8)  # Reset counter
            update_light()

        # Coffee
        if digitalRead(BUTTON_PIN):
            pots += 1
            update_coffee(pots)

        counter -= 1


def update_coffee(pots):
    blink(2)
    # Date formatted like '06. October 2014 13:13:19'
    coffee_date = datetime.datetime.now().strftime('%m. %B %Y %H:%M:%S')
    post('coffee', {'pots': pots, 'datetime': coffee_date})
    time.sleep(1)
    blink(2)
    if DEBUG:
        print 'New coffee pot:', coffee_date


def update_light():
    # 0 = On, apparantly
    if digitalRead(LIGHT_PIN) == 0:
        status = 'on'
    else:
        status = 'off'
    post('light', {'light': status})
    blink()
    if DEBUG:
        print 'Light level updated:', status


def post(relative_url, data):
    data['api_key'] = API_KEY
    r = requests.post(URL + relative_url, data=data)
    if DEBUG:
        print 'POST:', URL + relative_url


def setup():
    wiringPiSetup()
    pinMode(LED_PIN, OUTPUT)
    digitalWrite(LED_PIN, HIGH)
    pinMode(LIGHT_PIN, INPUT)
    pinMode(BUTTON_PIN, INPUT)


def blink(n=1):
    for _ in range(n):
        digitalWrite(LED_PIN, LOW)
        time.sleep(0.3)
        digitalWrite(LED_PIN, HIGH)
        time.sleep(0.3)

if __name__ == '__main__':
    main()
