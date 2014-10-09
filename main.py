#!/usr/bin/env python
import RPi.GPIO as GPIO
import datetime
import requests
import time
try:
    from settings import API_KEY, NAME, DEBUG
except ImportError:
    raise SystemExit('settings.py not found')


class Pin(object):
    URL = "http://passoa.online.ntnu.no/notiwire/" + NAME + '/'

    def post(self, data):
            data['api_key'] = API_KEY
            r = requests.post(URL + self.relative_url, data=data)
            if DEBUG:
                print 'POST:', URL + self.relative_url


class Coffee(Pin):
    pots = 0

    relative_url = 'coffee'

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        self.last = time.time()
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN, GPIO.RISING, callback=self.update, bouncetime=5000)

    def update(self, signal):
        self.pots += 1
        self.notipi.blink(2)
        # Date formatted like '06. October 2014 13:13:19'
        coffee_date = datetime.datetime.now().strftime('%m. %B %Y %H:%M:%S')
        self.post({'pots': self.pots, 'datetime': coffee_date})
        time.sleep(1)
        self.notipi.blink(2)
        if DEBUG:
            print 'New coffee pot:', coffee_date


class Light(Pin):
    relative_url = 'light'

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.LIGHT_PIN, GPIO.IN)
        GPIO.add_event_detect(PIN, GPIO.BOTH, callback=self.update, bouncetime=5000)

    def update(self, signal):
        print 'Light:', signal
        # 0 = On, apparantly
        # if digitalRead(LIGHT_PIN) == 0:
        #     status = 'on'
        # else:
        #     status = 'off'
        # post({'light': status})
        # blink()
        # if DEBUG:
        #     print 'Light level updated:', status


class Led(Pin):
    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.PIN, GPIO.OUT)

    def blink(n=1):
        for _ in range(n):
            GPIO.output(self.PIN, False)
            time.sleep(0.3)
            GPIO.output(self.PIN, True)
            time.sleep(0.3)


class Notipi(object):
    BUTTON_PIN = 9
    LIGHT_PIN = 10
    LED_PIN = 11

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.coffee = Coffee(self, self.BUTTON_PIN)
        self.light = Light(self, self.LIGHT_PIN)
        self.led = Led(self, self.LED_PIN)
        self.led.blink(5)

    def blink(*args, **kwargs):
        self.led(*args, **kwargs)


def main():
    notipi = Notipi()

if __name__ == '__main__':
    main()
