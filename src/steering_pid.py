#!/usr/bin/env python

from servo-control import Servo

servo = Servo()

def init():
    # bump into limit switches to find upper and lower limits
    servo.upper_lim = 180
    servo.lower_lim = 0
    pass


