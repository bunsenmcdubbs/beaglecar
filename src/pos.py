#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import time

# This script receives turn rates from the "chatter" topic
# and integrates to find a current heading relative to the
# initial heading

# function to return current time in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

# global variables
angle = 0 # angular position relative to start heading
last_time = 0 # time in milliseconds at the last integration

# receives data from topic and integrates rates to calculate 
# current heading
# TODO: timestamps
def callback(data):
    global angle
    global last_time
    # gets the current time and calculates the seconds elapsed
    # since the last integration
    curr_time = current_milli_time()
    t_elapsed = (curr_time - last_time) / 1000.
    last_time = curr_time
    # print(str(t_elapsed))
    # integration!
    angle = angle + data.data * t_elapsed
    # logging current heading
    rospy.loginfo(rospy.get_name() + "\n" + str(angle))

# ROS Code
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    last_time = current_milli_time()
    listener()
