#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import math
from servo_controller import Servo

# most of the time.sleep calls work to give the servo
# time to respond (not instantaneous)

# setting up the limit switch pins
pin1 = "P8_12"
pin2 = "P8_14"
GPIO.setup(pin1, GPIO.IN)
GPIO.setup(pin2, GPIO.IN)

# starting the servo
servo = Servo()
servo.start()

# guessed center point
center = 100
# current angle
angle = center
# left and right limits
limit1 = angle
limit2 = angle

# turning left
while not GPIO.input(pin1) and not GPIO.input(pin2):
    angle += .01
    servo.set_angle(angle)
    time.sleep(.0001)
limit1 = angle
time.sleep(1)

# resetting servo to guessed center
angle = center
servo.set_angle(angle)
time.sleep(.2)

# turning right
while not GPIO.input(pin1) and not GPIO.input(pin2):
    angle -= .01
    servo.set_angle(angle)
    time.sleep(.0001)
limit2 = angle
time.sleep(1)

# calculating center from left and right limits
center = (limit1 + limit2) / 2
servo.set_angle(center)

print "limit1 = " + str(limit1) + " limit2 = " + str(limit2)
print "center = " + str(center)

time.sleep(1)

servo.stop()
