import rospy, simplekml
from geomedsftry_msgs.msg import Pose2D, Vector3

kml = simplekml.Kml()

origin = Pose2D()
origin.x = -71.43945
origin.y = 42.44345
origin.theta = 0

# conversion factors around Acton long lat
# long lat to meters
long_conv = 82000
lat_conv = 111200

def guesslog(pose):
  

def gpslog(sat):
  

def main():
  rospy.Subscriber("loc", Pose2D, guesslog)
  rospy.Subscriber("fix", NavSatFix, gpslog)
  rospy.spin()

if __name__=="__main__":
  main()
