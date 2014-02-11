#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32 # ROS Float32 message type
from Adafruit_I2C import Adafruit_I2C # Adafruit_BBIO lib's I2C

# Wakes up the device by writing 0 to address 0x6b
# need to implement bit masks to only flip bit 6
def wake(i2c):
    i2c.write8(0x6b, 0)

# Puts the device to sleep
# TODO: flip bit 6 on 0x6b to 1
def sleep(i2c):
    print("Sleepy time... need to implement")

# Calibrates the gyroscope by taking 100 readings
# and averaging the values to achieve a "zero point"
# The device must be still for calibration
def zero(i2c):
    sum = 0
    for x in range(0,200):
        sum += read(i2c, 0)
    zeroPoint = sum / 200.
    # print ("zero point = " + str(zeroPoint))
    return zeroPoint

# Reads the 2 byte signed value from the device's z axis gyro
# and returns an adjusted value in degrees per second
# TODO need to automate the scale factor (different settings)
def read(i2c, zeroPoint = 0):
    msb = i2c.readS8(0x47) # Most significant byte
    lsb = i2c.readU8(0x48) # Least significant byte
    raw = msb * 256 + lsb
    # print ("raw = " + str(raw/131.))
    # print ("zero point = " + str(zeroPoint))
    # uses the "zero point" calibration value to correct
    # the raw reading after converting to degrees per second
    rot = raw / 131. - zeroPoint
    return rot

# ROS code
def talker(i2c):
    # starts publisher on topic 'chatter'
    # and data type Float 32
    pub = rospy.Publisher('turn_rate', Float32)
    # starts the node with name "talker"
    rospy.init_node('talker')
    # wakes up the i2c device
    wake(i2c)
    # finds the calibration point
    zeroPoint = zero(i2c)
    while not rospy.is_shutdown():
        # reads a calibrated z axis turn rate
        turn_rate = read(i2c, zeroPoint)
        # logs the turn rate (printing to console as well)
        rospy.loginfo(turn_rate)
        # publishes the turn rate to the topic
        pub.publish(turn_rate)
        # wait for 0.001 sec
        rospy.sleep(0.001)
    # after the ROS node is closed, put the device
    # back into sleep mode
    sleep(i2c)

if __name__ == '__main__':
    try:
        i2c = Adafruit_I2C(0x68) # initializing the i2c device
        talker(i2c) # ROS Stuff
    except rospy.ROSInterruptException:
        pass
