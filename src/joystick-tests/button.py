#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time

pin = "P8_12"
GPIO.setup(pin, GPIO.IN)

switch_state = 0

while True:
    GPIO.wait_for_edge(pin, GPIO.RISING)
    print ("pressed")
