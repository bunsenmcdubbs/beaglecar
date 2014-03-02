#!/usr/bin/env python
import rospy
import Adafruit_BBIO.GPIO as GPIO
from servo_controller import Servo
from sensor_msgs.msg import Joy

def callback(data):
    global center
    global span
    # map [-1,1] to [-90,90]
    # 0deg = straight forward
    angle = span * data.axes[0]
    # set servo angle
    servo.set_angle(angle + center)
    return

def start():
    # Starting servo controller
    global servo
    servo = Servo() # using default values
    servo.start()
    init_servo()
    global center
    center = 90
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
    span = limit1 - limit2
    servo.set_angle(center)

if __name__ == '__main__':
    start()
