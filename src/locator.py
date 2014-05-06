#!/usr/bin/env python
import rospy, time, math
from sensor_msgs.msg import Imu, NavSatFix
from geometry_msgs.msg import Pose2D, Vector3

# current velocity (from integration and GPS)
vel = 0 # meters / second
twist = 0 # radians / second

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

# updates the time and returns the elapsed time
def updateTime(new_time):
  global time
  elapsed_time = new_time.secs-time.secs + 0.000000001*(new_time.nsecs - time.nsecs)
  time = new_time
  return elapsed_time

# recieves and handles gps data from "fix" topic
def gps(loc):
  # get the time elapsed
  timeElapsed = updateTime(loc.header.stamp)
  
  # calculating easting and northing relative to arbitrary
  # origin point in meters
  easting = (loc.longitude - origin.x) * long_conv
  northing = (loc.latitude - origin.y) * lat_conv
  
  
  # default trust values
  # gps = raw gps data
  # imu = dead reckoning estimates
  gpsTrust = 0.9
  imuTrust = 0.1
  
  # special edge case if the car is in initialization
  # first estimate is 100% GPS
  global init_phase
  if init_phase:
    init_phase = False
    gpsTrust = 1.0
    imuTrust = 0.0
    print "initialization phase"
  
  else: 
    global jumping, pose, imu_pose
    # trying to predict where the car should be from imu data => velocity
    # very similar to the regular imu updates but changed slightly
    xGuess = math.cos(pose.theta) * (vel * timeElapsed) + imu_pose.x
    yGuess = math.sin(pose.theta) * (vel * timeElapsed) + imu_pose.y
    tGuess = twist * timeElapsed + imu_pose.theta
    
    # if current estimate is more than 3 meters away from gps ... JUMP!
    if math.pow(xGuess - easting, 2) + math.pow(yGuess - northing, 2) > 9:
      # jump detected
      print "***JUMP***"
      jumping = True
      gpsTrust = 0.2
      imuTrust = 0.8
    else:
      jumping = False
      
  # calculate the weighted average between gps and imu guesses
  pose.x = easting * gpsTrust + imu_pose.x * imuTrust
  pose.y = northing * gpsTrust + imu_pose.y * imuTrust
  # continue for heading estimate when not jumping
  if not jumping:
    pose.theta = math.atan2(northing, easting) * gpsTrust + imu_pose.theta * imuTrust
  
  # reset the imu/dead reckoning guess to the latest estimate
  imu_pose = pose
  
  # publish
  global pub
  rospy.loginfo(pose)
  pub.publish(pose)

  return

# IMPLEMENT!!!
def imu(twist):
  return

def main():
  # sets the navigation mode for initilization (primarily for gps handling)
  global init_phase
  init_phase = True
  # subscribes to GPS and IMU topics
  rospy.Subscriber("fix", NavSatFix, gps) # GPS
  rospy.Subscriber("mpu6050", Imu, imu) # IMU
  # sets up the publisher
  global pub
  pub = rospy.Publisher('loc', Pose2D) # publishes Pose2D messages on the loc topic
  rospy.init_node('locator')
  
  global time
  time = rospy.get_rostime()

  rospy.spin()

if __name__ == "__main__":
  main()
