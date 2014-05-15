#!/usr/bin/env python
import rospy, math
from servo_controller import Servo
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

class Car:
  def __init__(self, s_pin = "P8_13", f_pin = "P9_14", b_pin = "P9_22", debug = False):
    # initialize servo for steering
    self.steer = Servo(s_pin)
    # save PWM pins for forward and reverse
    self.forward = f_pin
    self.reverse = b_pin
    # start servos and motors
    self.start()
    # center the steering
    center_steering()

  # set the "steering wheel" of the car
  # negative is left
  # positive is right
  def turn(self, angle = 0):
    self.steer.set_angle(self.center + angle)
    if debug:
      print angle
    return

  # set the car speed
  def set_speed(self, speed):
    speed = clamp(speed, -100, 100)
    if speed > 0:
        PWM.set_duty_cycle(reverse, 0)
        PWM.set_duty_cycle(forward, speed)
    else:
        PWM.set_duty_cycle(forward, 0)
        PWM.set_duty_cycle(reverse, -speed)
    return

  # start PWM lines for forward and reverse and start steering servo
  def start(self):
    PWM.start(self.forward, 0, 200)
    PWM.start(self.reverse, 0, 200)
    self.steer.start()
    return

  # stop PWM lines for forward and reverse and stop steering servo
  def stop(self):
    PWM.stop(self.forward)
    PWM.stop(self.reverse)
    self.steer.stop()
    PWM.cleanup()
    return

  # center the steering servo between two limit switches
  def center_steering():
    pin1 = "P8_12"
    pin2 = "P8_14"
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)

    # guessed center point
    center = 100
    # current angle
    angle = center
    # left and right limits
    limit1 = angle
    limit2 = angle
    # turning left
    while not GPIO.input(pin1) and not GPIO.input(pin2):
        angle += .5
        self.steer.set_angle(angle)
        time.sleep(.05)
    limit1 = angle
    time.sleep(.5)

    # resetting servo to guessed center
    angle = center
    servo.set_angle(angle)
    time.sleep(.2)

    # turning right
    while not GPIO.input(pin1) and not GPIO.input(pin2):
        angle -= .5
        self.steer.set_angle(angle)
        time.sleep(.05)
    limit2 = angle
    time.sleep(.5)

    # calculating center from left and right limits
    self.center = (limit1 + limit2) / 2
    # calculate total range (102% of limit differences)
    self.span = (limit1 - limit2) / 2 * 1.02 # allow for a little extra wiggle
    self.steer.set_limits(limit2, limit1)

    if debug:
      print "center = " + str(center)
      print "span = " + str(span)
    servo.set_angle(center)
    return

  # clamp x value between specified min and max values
  def clamp(x, min, max):
    if min > max:
      return False
    if x > max:
      return max
    if x < min:
      return min
    return x
