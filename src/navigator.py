import rospy, time
from sensor_msgs.msg import Imu, NavSatFix
from geometry_msgs.msg import Pose2D, Vector3

# current velocity (from integration and GPS)
vel = 0
twist = 0

# current pose (position and direction)
# in easting and northing from origin
pose = Pose2D()
pose.x, pose.y, pose.theta = 0

imu_pose = Pose2D()
imu_pose.x, imu_pose.y, imu_pose.theta = 0

origin = Pose2D()
origin.x = -71.43945
origin.y = 42.44345
origin.theta = 0

# conversion factors around Acton long lat
# long lat to meters
long_conv = 82000
lat_conv = 111200

# current target (ignore direction)
target = Pose2D
target.x, target.y, target.theta = 0

time

jumping = False

def checkJump():
  return jumping

def updateTime(new_time):
  elapsed_time = new_time.sec-time.sec + 0.000000001*(new_time.nsec - time.nsec)
  time = new_time
  return elapsed_time

def gps(loc):
  timeElapsed = updateTime(loc.stamp)
  easting = (loc.longitude - origin.x) * long_conv
  northing = (loc.latitude - origin.y) * lat_conv
  
  global jumping, pose, imu_pose
  xGuess = math.cos(pose.theta) * (vel * timeElapsed) + pose.x
  yGuess = math.sin(pose.theta) * (vel * timeElapsed) + pose.y
  
  gpsTrust = 0.9
  imuTrust = 0.1
  
  # if current estimate is more than 3 meters away from gps ... JUMP!
  if math.pow(xGuess - easting, 2) + math.pow(yGuess - northing, 2) > 9:
    # jump detected
    jumping = True
    gpsTrust = 0.2
    imuTrust = 0.8

  pose.x = easting * gpsTrust + imu_pose.x * imuTrust
  pose.y = northing * gpsTrust + imu_pose.y * imuTrust
  
  imu_pose = pose
  return

# IMPLEMENT!!!
def imu(twist):
  return

def main():
  rospy.Subscriber("fix", NavSatFix, gps)
  rospy.Subscriber("mpu6050", Imu, imu)
  
  global pub
  pub = rospy.Publisher('loc', Imu)
  rospy.init_node('navigator')
  
  global time
  time = rospy.get_rostime()

if __name__ == "__main__":
  main()
