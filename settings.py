import RPi.GPIO as GPIO

API_URL = 'https://passoa.online.ntnu.no/notipi/'

BUTTON_PIN = 9
LIGHT_PIN = 10
LED_PIN = 11

# Direction for lights on
LIGHT_DIRECTION = GPIO.LOW
# Pull up down
COFFEE_PUD = GPIO.PUD_UP

NAME = 'DEBUG'
API_KEY = '123'

DEBUG = 1

try:
    from local import *
except ImportError:
    raise SystemExit('local.py not found')
