#!/usr/bin/env python
import RPi.GPIO as GPIO
import datetime
import logging
import requests
import settings
import time
import threading


class Pin(object):
    URL = settings.API_URL + settings.NAME + '/'

    def post(self, data=None):
            logging.debug('Ready to send a POST request for {url} with data {data}'.format(url=self.relative_url, data=data))
            if not data:
                data = {}
            data['api_key'] = settings.API_KEY
            r = requests.post(self.URL + self.relative_url, data=data)
            logging.debug('POST Request sent with response {response}'.format(response=r.text))


class Coffee(Pin):
    pots = 0

    relative_url = 'coffee'

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=settings.COFFEE_PUD)
        # Running in it's own thread
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.update, bouncetime=5000)
        logging.info('Coffee button is ready')

    def update(self, signal):
        self.notipi.blink(2)
        self.post()
        time.sleep(1)
        self.notipi.blink(2)
        logging.info('New coffee pot at {date}'.format(date=datetime.datetime.now()))


class Light(Pin):
    relative_url = 'status'
    interval = 60 * 30  # 30min

    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN
        self.status = None

        GPIO.setup(self.PIN, GPIO.IN)
        # Running in it's own thread
        GPIO.add_event_detect(self.PIN, GPIO.BOTH, callback=self.update)
        # Update once every hour too
        self.periodic_update()
        logging.info('Light sensor is ready')

    def update(self, signal=0):
        time.sleep(0.2)
        if GPIO.input(self.PIN) == settings.LIGHT_DIRECTION:
            status = 'true'
        else:
            status = 'false'
        # Only update if status has changed
        if self.status != status:
            self.status = status
            self.post({'status': status})
            self.notipi.blink()
            logging.debug('Light status changed to {status}'.format(status=self.status))

    def periodic_update(self):
        self.update()
        threading.Timer(self.interval, self.periodic_update).start()


class Led(Pin):
    def __init__(self, notipi, PIN):
        self.notipi = notipi
        self.PIN = PIN

        GPIO.setup(self.PIN, GPIO.OUT)
        logging.info('LED is ready')

    def blink(self, n=1):
        for _ in range(n):
            GPIO.output(self.PIN, False)
            time.sleep(0.3)
            GPIO.output(self.PIN, True)
            time.sleep(0.3)
        logging.debug('LED blinked {times} time(s)'.format(times=n))


class Notipi(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.led = Led(self, settings.LED_PIN)
        self.coffee = Coffee(self, settings.BUTTON_PIN)
        self.light = Light(self, settings.LIGHT_PIN)
        self.blink(5)

    def blink(self, *args, **kwargs):
        self.led.blink(*args, **kwargs)


def main():
    # Logging
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    logging.info('Starting NotiPi')
    notipi = Notipi()
    logging.info('NotPi handlers started')
    # Wait forever
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
