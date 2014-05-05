#!/usr/bin/env python
import rospy, time, math
from sensor_msgs.msg import Imu, NavSatFix
from geometry_msgs.msg import Pose2D, Vector3

# current velocity (from integration and GPS)
vel = 0
twist = 0

# current pose (position and direction)
# in easting and northing from origin
pose = Pose2D()
imu_pose = Pose2D()

origin = Pose2D()
origin.x = -71.43945
origin.y = 42.44345
origin.theta = 0

# conversion factors around Acton long lat
# long lat to meters
long_conv = 82000
lat_conv = 111200

# current target (ignore direction)
target = Pose2D()

time

jumping = False

def checkJump():
  return jumping

def updateTime(new_time):
  global time
  elapsed_time = new_time.secs-time.secs + 0.000000001*(new_time.nsecs - time.nsecs)
  time = new_time
  return elapsed_time

def gps(loc):
  timeElapsed = updateTime(loc.header.stamp)
  easting = (loc.longitude - origin.x) * long_conv
  northing = (loc.latitude - origin.y) * lat_conv

  gpsTrust = 0.9
  imuTrust = 0.1
  
  global init_phase
  if init_phase:
    init_phase = False
    gpsTrust = 1.0
    imuTrust = 0.0
    print "initialization phase"
  
  else: 
    global jumping, pose, imu_pose
    xGuess = math.cos(pose.theta) * (vel * timeElapsed) + pose.x
    yGuess = math.sin(pose.theta) * (vel * timeElapsed) + pose.y
  
    gpsTrust = 0.9
    imuTrust = 0.1
  
    # if current estimate is more than 3 meters away from gps ... JUMP!
    if math.pow(xGuess - easting, 2) + math.pow(yGuess - northing, 2) > 9:
      # jump detected
      print "***JUMP***"
      jumping = True
      gpsTrust = 0.2
      imuTrust = 0.8

  pose.x = easting * gpsTrust + imu_pose.x * imuTrust
  pose.y = northing * gpsTrust + imu_pose.y * imuTrust
  
  imu_pose = pose

  global pub
  rospy.loginfo(pose)
  pub.publish(pose)

  return

# IMPLEMENT!!!
def imu(twist):
  return

def main():
  global init_phase
  init_phase = True

  rospy.Subscriber("fix", NavSatFix, gps)
  rospy.Subscriber("mpu6050", Imu, imu)

  global pub
  pub = rospy.Publisher('loc', Pose2D)
  rospy.init_node('navigator')
  
  global time
  time = rospy.get_rostime()

  rospy.spin()

if __name__ == "__main__":
  main()
