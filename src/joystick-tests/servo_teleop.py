#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy

def callback(data):
    # map [-1,1] to [-90,90]
    angle = 90 * data.axes[0]
    # set servo angle
    servo.set_angle(angle)
    return

def start():
    # Starting servo controller
    global servo
    servo = Servo() # using default values
    servo.start()
    # Subscribe to ROS Joy node
    rospy.Subscriber("joy", Joy, callback)
    rospy.init_node("Joy2Servo")
    rospy.spin()
    

if __name__ == '__main__':
    start()
