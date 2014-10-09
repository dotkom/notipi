#!/usr/bin/env python
import RPi.GPIO as GPIO
import datetime
import requests
import time
try:
    from settings import API_KEY, NAME, DEBUG
except ImportError:
    raise SystemExit('settings.py not found')


BUTTON_PIN = 9
LIGHT_PIN = 10
LED_PIN = 11

INPUT = 0
OUTPUT = 1

HIGH = 1
LOW = 0

PUD_UP = 2

URL = "http://passoa.online.ntnu.no/notiwire/" + NAME + '/'


class Coffee(object):
    def __init__(self):
        self.pots = 0
        GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)
        GPIO.add_event_callback(BUTTON_PIN, self.update)

    def update(self):
        print 'New pot!', self.pots


def main():
    setup()
    counter = 0
    pots = 0
    now = time.time()
    blink(10)
    coffee = Coffee()
    while True:
        # Light
        if now + 20 < time.time():
            now = time.time()  # Reset timer
            update_light()

        # # Coffee
        # if digitalRead(BUTTON_PIN) == 0:
        #     pots += 1
        #     update_coffee(pots)


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
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIGHT_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)

    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)


def blink(n=1):
    for _ in range(n):
        GPIO.output(LED_PIN, LOW)
        time.sleep(0.3)
        GPIO.output(LED_PIN, HIGH)
        time.sleep(0.3)

if __name__ == '__main__':
    main()
