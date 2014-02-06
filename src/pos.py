#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import time

current_milli_time = lambda: int(round(time.time() * 1000))

angle = 0
last_time = 0

def callback(data):
    global angle
    global last_time
    curr_time = current_milli_time()
    t_elapsed = (curr_time - last_time) / 1000.
    print(str(t_elapsed))
    angle = angle + data.data * t_elapsed
    rospy.loginfo(rospy.get_name() + "\n" + str(angle))


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    last_time = current_milli_time()
    listener()
