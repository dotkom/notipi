API_URL = 'https://passoa.online.ntnu.no/notipi/'
ZWAVE_URL = 'localhost:8083/ZAutomation/api/v1/devices/'


NAME = 'DEBUG'
API_KEY = '123'

ZWAVE_USER = ''
ZWAVE_PASSWORD = ''

DEBUG = 1

try:
    from local import *
except ImportError:
    raise SystemExit('local.py not found')
