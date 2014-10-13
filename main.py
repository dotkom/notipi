#!/usr/bin/env python
import RPi.GPIO as GPIO
import datetime
import requests
import settings
import time


class Pin(object):
    URL = "http://passoa.online.ntnu.no/notiwire/" + settings.NAME + '/'

    def post(self, data):
            data['api_key'] = settings.API_KEY
            r = requests.post(self.URL + self.relative_url, data=data)
            if settings.DEBUG:
                print 'POST:', self.URL + self.relative_url


class Coffee(Pin):
    pots = 0

    relative_url = 'coffee'

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        self.last = time.time()
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Running in it's own thread
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.update, bouncetime=5000)

    def update(self, signal):
        self.pots += 1
        self.notipi.blink(2)
        # Date formatted like '06. October 2014 13:13:19'
        coffee_date = datetime.datetime.now().strftime('%m. %B %Y %H:%M:%S')
        self.post({'pots': self.pots, 'datetime': coffee_date})
        time.sleep(1)
        self.notipi.blink(2)
        if settings.DEBUG:
            print 'New coffee pot:', coffee_date


class Light(Pin):
    relative_url = 'light'

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.PIN, GPIO.IN)
        # Running in it's own thread
        GPIO.add_event_detect(self.PIN, GPIO.BOTH, callback=self.update)

    def update(self, signal):
        time.sleep(0.2)
        if GPIO.input(self.PIN) == GPIO.LOW:
            status = 'on'
        else:
            status = 'off'
        self.post({'light': status})
        self.notipi.blink()
        if settings.DEBUG:
            print 'Light status updated:', status


class Led(Pin):
    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.PIN, GPIO.OUT)

    def blink(self, n=1):
        for _ in range(n):
            GPIO.output(self.PIN, False)
            time.sleep(0.3)
            GPIO.output(self.PIN, True)
            time.sleep(0.3)


class Notipi(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.coffee = Coffee(self, settings.BUTTON_PIN)
        self.light = Light(self, settings.LIGHT_PIN)
        self.led = Led(self, settings.LED_PIN)
        self.blink(5)

    def blink(self, *args, **kwargs):
        self.led.blink(*args, **kwargs)


def main():
    notipi = Notipi()
    # Wait forever
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
