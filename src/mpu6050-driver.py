#!/usr/bin/env python
import rospy
import time
from Adafruit_I2C import Adafruit_I2C
from sensor_msgs.msg import Imu
from std_msgs.msg import Header, Float64, Time
from geometry_msgs.msg import Vector3

# x, y, z in MSB, LSB order
accel = [[0x3b, 0x3c], [0x3d, 0x3e], [0x3f, 0x40]]
gyro = [[0x43, 0x44], [0x45, 0x46], [0x47, 0x48]]
# MSB, LSB
temp = [0x41, 0x42]

current_time = lambda: int(round(time.time()))

def read (imu, addr, scale = 1.0, bias = 0.0):
  "Reads data from addresses specified [MSB, LSB] and returns a decimal"
  raw = [imu.readS8(addr[0]), imu.readU8(addr[1])]
  combined = raw[0] * 256 + raw[1]
  return combined / scale - bias

def calibrate (imu, addrs, samples = 100, freq = 10.):
  "Averages a number of samples taken at a certain frequency over addresses"
  global zeros
  zeros = [0] * len(addrs)

  if samples == 0:
    return zeros

  for sample in range (0, samples):
    for i in range(0, len(addrs)):
      addr = addrs[i]
      zeros[i] += read(imu, addr)
    time.sleep(1/freq)

  for total in zeros:
    total /= samples

  return zeros

def make_header():
  global seq
  header = Header()
  header.seq = seq
  seq += 1
  time = Time()
  time.data = current_time();
  header.stamp = time
  header.frame_id = "0"
  return header

def read_gyros():
  return read_mult(gyro, scale=131.)

def read_accels():
  return read_mult(accel, scale=16384.)

def read_mult(addrs, scale=1):
  result = Vector3()
  vals = []
  for i in range(len(addrs)):
    ##vals.append(read(imu, addrs[i], bias = zeros[error_index+i]))
    vals.append(read(imu, addrs[i], scale))
  result.x, result.y, result.z = vals
  return result

def talker():

  global pub
  pub = rospy.Publisher('mpu6050', Imu)
  rospy.init_node('MPU6050-Driver')

  #calibrate(imu, accel+gyro, samples = 0)

  global seq
  seq = 0

  while not rospy.is_shutdown():
    sample = Imu()
    sample.header = make_header()
    sample.orientation_covariance[0] = -1
    sample.angular_velocity_covariance = [0]*9
    sample.angular_velocity = read_gyros()
    sample.linear_acceleration_covariance = [0]*9
    sample.linear_acceleration = read_accels()

    rospy.loginfo(str(sample))
    pub.publish(sample)
    time.sleep(0.1)

if __name__ == "__main__":
  try:
      global imu
      imu = Adafruit_I2C(0x68) # initializing the i2c device
      imu.write8(0x6b, 0) # waking the imu
      talker() # ROS Stuff
  except rospy.ROSInterruptException:
      pass
