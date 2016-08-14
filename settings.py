API_URL = 'https://passoa.online.ntnu.no/notipi/'
ZWAVE_URL_LIGHT = 'http://129.241.104.252:8083/ZAutomation/api/v1/devices/ZWayVDev_zway_2-0-50-2'


NAME = ''
API_KEY = ''

ZWAVE_USER = ''
ZWAVE_PASSWORD = ''

DEBUG = 1

try:
    from local import *
except ImportError:
    raise SystemExit('local.py not found')
