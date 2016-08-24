API_URL = 'https://passoa.online.ntnu.no/notipi/'
ZWAVE_URL_LIGHT = ''
ZWAVE_URL_COFFEE = ''

NAME = ''
API_KEY = ''

ZWAVE_USER = ''
ZWAVE_PASSWORD = ''

POLLING_FREQUENCY = 10

DEBUG = 1

try:
    from local import *
except ImportError:
    raise SystemExit('local.py not found')
