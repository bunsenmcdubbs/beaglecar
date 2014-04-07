#!/usr/bin/env python
import rospy
import sys
from sensor_msgs.msg import NavSatFix

count = 60.
curr_count = 0
lon = 0
lat = 0

def callback (loc):
    global curr_count
    global lon
    global lat
    if curr_count >= count :
        print "final average " + str(lat) + ", " + str(lon)
        sys.exit()
    curr_count += 1
    tlon = loc.longitude
    tlat = loc.latitude
    print str(curr_count) + " " + str(tlat) + ", " + str(tlon)
    lon += tlon / count
    lat += tlat / count

def main ():
    rospy.Subscriber("fix", NavSatFix, callback)
    rospy.init_node("GPS_AVG")
    rospy.spin()

if __name__ == '__main__':
    main()
