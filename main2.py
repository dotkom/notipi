#!/usr/bin/env python
import datetime
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
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        last_update = 0
        auth = HTTPBasicAuth(settings.ZWAVE_USER, settings.ZWAVE_PASSWORD)
        while True:
            time.sleep(settings.POLLING_FREQUENCY)
            if self.stopped:
                return
            try:
                requests.get(settings.ZWAVE_URL_COFFEE + '/command/update', auth=auth)
                r = requests.get(settings.ZWAVE_URL_COFFEE, auth=auth)
                json = r.json()['data']
                current_update = json['updateTime']
                current_effect = json['metrics']['level']
                if current_update == last_update:
                    logging.info("Coffeesensor is unpowered")
                    last_update = current_update
                    continue
                if current_effect > 1000:
                    # COFFEE IS BOILING
                    update_notiwire(relative_url='coffee')
                    logging.info('New coffee pot at {date}'.format(date=datetime.datetime.now()))
                    last_update = current_update
                    time.sleep(60 * 10)
                    continue
                last_update = current_update

            except requests.exceptions.RequestException as e:
                logging.error(e)

    def stop(self):
        self.stopped = True


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
        last_update = 0
        last_update_to_notiwire = 0
        auth = HTTPBasicAuth(settings.ZWAVE_USER, settings.ZWAVE_PASSWORD)
        while True:
            time.sleep(settings.POLLING_FREQUENCY)
            if self.stopped:
                return
            try:
                requests.get(settings.ZWAVE_URL_LIGHT + '/command/update', auth=auth)
                r = requests.get(settings.ZWAVE_URL_LIGHT, auth=auth)
                json = r.json()['data']
                current_update = json['updateTime']

                if current_update == last_update:
                    status = 'false'
                    logging.info('lights are off')
                else:
                    status = 'true'
                    logging.info('lights are on')

                # Update if light changes, or last update was more than 30 minutes ago
                if status != self.status or time.time() - last_update_to_notiwire > 60 * 30:
                    self.status = status
                    logging.info("Lightstatus changed at {date}, light status is now {status}"
                                 .format(date=datetime.datetime.now(), status=status))
                    update_notiwire(data={'status': status}, relative_url='status')
                    last_update_to_notiwire = time.time()

                last_update = current_update

            except requests.exceptions.RequestException as e:
                logging.error(e)

    def stop(self):
        self.stopped = True


class Notipi(object):
    def __init__(self):
        Light().start()
        Coffe().start()


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
