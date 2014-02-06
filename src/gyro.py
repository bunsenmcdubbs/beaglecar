#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from Adafruit_I2C import Adafruit_I2C


def wake(i2c):
    i2c.write8(0x6b, 0)

def sleep(i2c):
    print("Sleepy time... need to implement")

def zero(i2c):
    sum = 0
    for x in range(0,100):
        sum += read(i2c, 0)
    zeroPoint = sum / 100.
    print ("zero point = " + str(zeroPoint))
    return zeroPoint

def read(i2c, zeroPoint = 0):
    b = i2c.readS8(0x47)
    s = i2c.readU8(0x48)
    raw = b * 256 + s
    print ("raw = " + str(raw/131.))
    print ("zero point = " + str(zeroPoint))
    rot = raw / 131. - zeroPoint
    return rot

def talker(i2c):
    pub = rospy.Publisher('chatter', Float32)
    rospy.init_node('talker')
    wake(i2c)
    zeroPoint = zero(i2c)
    while not rospy.is_shutdown():
        str = read(i2c, zeroPoint)
        rospy.loginfo(str)
        pub.publish(str)
        rospy.sleep(0.001)
    sleep(i2c)

if __name__ == '__main__':
    try:
        i2c = Adafruit_I2C(0x68)
        talker(i2c)
    except rospy.ROSInterruptException:
        pass
