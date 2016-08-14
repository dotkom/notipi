#!/usr/bin/env python
import logging
import time
from threading import Thread

import requests
from requests.auth import HTTPBasicAuth

import settings


def update_notiwire(data=None, relative_url=''):
    URL = settings.API_URL + settings.NAME + '/'
    if not data:
        data = {}
    data['api_key'] = settings.API_KEY
    logging.debug('Ready to send a POST request for {url} with data {data}'.format(url=relative_url, data=data))
    r = requests.post(URL + relative_url, data=data)
    logging.debug('POST Request sent with response {response}'.format(response=r.text))


class Coffe:
    def __init__(self):
        pass


class Light:
    def __init__(self):
        self.stopped = False
        self.status = 'false'

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        last_update = 0 # TODO initialize with current value?
        auth = HTTPBasicAuth(settings.ZWAVE_USER, settings.ZWAVE_PASSWORD)
        while True:
            time.sleep(10)
            if self.stopped:
                return
            try:
                requests.get(settings.ZWAVE_URL_LIGHT+'/command/update', auth=auth)
                r = requests.get(settings.ZWAVE_URL_LIGHT, auth=auth)
                json = r.json()['data']
                current_update = json['updateTime']

                if current_update == last_update:
                    status = 'false'
                    logging.info('lights are off')
                else:
                    status = 'true'
                    logging.info('lights are on')
                if status != self.status:
                    self.status = status
                    update_notiwire(data={'status': status}, relative_url='status')

                last_update = current_update

            except requests.exceptions.RequestException as e:
                logging.error(e)

    def stop(self):
        self.stopped = True


class Notipi(object):
    def __init__(self):
        light = Light().start()
        # coffe = Coffe().start()


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
