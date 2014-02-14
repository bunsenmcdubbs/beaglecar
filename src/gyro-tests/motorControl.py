#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import time
import Adafruit_BBIO.PWM as PWM

# This script receives turn rates from the "chatter" topic
# and integrates it to find the current relative angle.
# Then it converts the angle to a PWM signal to drive a 
# motor controller.

# servo variables
pwm_pin = "P8_13"
duty_min = 0
duty_max = 100
duty_span = duty_max - duty_min

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
    # turn servo
    set_angle(clamp(angle,0,100))
    # logging current heading
    rospy.loginfo(rospy.get_name() + "  " + str(angle))

def clamp(x, min = 0, max = 100):
    if x < min:
        return min
    if x > max:
        return max
    return x

# ROS Code
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("turn_rate", Float32, callback)
    rospy.spin()
    print ("test")
    PWM.stop(pwm_pin)
    PWM.cleanup()

def set_angle(x = 50):
    PWM.set_duty_cycle(pwm_pin, float(x))

if __name__ == '__main__':
    PWM.start(pwm_pin, duty_max, 60.0)
    set_angle()
    last_time = current_milli_time()
    listener()
