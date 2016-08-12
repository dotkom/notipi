#!/usr/bin/env python
import datetime
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import settings
import time
from threading import Thread


class Coffe:
    def __init__(self):
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            time.sleep(5)
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            try:
                r = requests.get(settings.ZWAVE_URL, auth=HTTPBasicAuth('user', 'pass'))
                data = r.json()
                print data
            except:
                # TODO: HANDLE EXCEPTIONS
                pass

    def stop(self):
        self.stopped = True



class Notipi(object):
    def __init__(self):
        coffe = Coffe().start()
        # self.light = Light(self)


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
