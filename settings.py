API_URL = 'https://passoa.online.ntnu.no/notipi/'

BUTTON_PIN = 9
LIGHT_PIN = 10
LED_PIN = 11

NAME = 'DEBUG'
API_KEY = '123'

DEBUG = 1

try:
    from local import *
except ImportError:
    raise SystemExit('local.py not found')
