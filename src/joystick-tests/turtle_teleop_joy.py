#!/usr/bin/env python
import rospy
#import Adafruit_BBIO.PWM as PWM
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

pub = rospy.Publisher('turtle1/cmd_vel', Twist)

def callback(data):
    twist = Twist()
    twist.linear.x = 4*data.axes[1]
    twist.angular.z = 4*data.axes[0]
    pub.publish(twist)

def talker():
    global pub
    pub = rospy.Publisher('turtle1/cmd_vel', Twist)
    rospy.Subscriber("joy", Joy, callback)
    rospy.init_node('talker')
    rospy.spin()

if __name__ == '__main__':
    talker()

