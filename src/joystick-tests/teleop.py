#!/usr/bin/env python
import rospy
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from servo_controller import Servo
from sensor_msgs.msg import Joy

def callback(data):
    if data.buttons[8]:
        exit()
        return
    # map [-1,1] to [-90,90]
    # 0deg = straight forward
    angle = span * data.axes[0]
    # set servo angle
    servo.set_angle(angle + center)
    speed = 100 * data.axes[3]
    if speed > 0:
        PWM.set_duty_cycle(reverse, 0)
        PWM.set_duty_cycle(forward, speed)
    else:
        PWM.set_duty_cycle(forward, 0)
        PWM.set_duty_cycle(reverse, -speed)
    return

def exit():
    servo.stop()
    PWM.stop(forward)
    PWM.stop(reverse)
    PWM.cleanup()
    return

def start():
    # Starting servo controller
    global servo
    servo = Servo() # using default values
    servo.start()
    # Start motor control
    global forward
    global reverse
    global PWM
    forward = "P9_14"
    reverse = "P9_22"
    PWM.start(forward, 0, 200)
    PWM.start(reverse, 0, 200)
    # initializing the servo
    init_servo()
    # Subscribe to ROS Joy node
    rospy.Subscriber("joy", Joy, callback)
    rospy.init_node("Joy2Servo")
    rospy.spin()
    
def init_servo():
    global center
    global span
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
        servo.set_angle(angle)
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
        servo.set_angle(angle)
        time.sleep(.05)
    limit2 = angle
    time.sleep(.5)

    # calculating center from left and right limits
    center = (limit1 + limit2) / 2
    span = (limit1 - limit2) / 2 * 1.02
    print "center = " + str(center)
    print "span = " + str(span)
    servo.set_angle(center)

if __name__ == '__main__':
    start()
