#!/usr/bin/env python
import rospy
import sys
from sensor_msgs.msg import NavSatFix

count = 300.
curr_count = 0
a = []

def callback (loc):
    global curr_count
    if curr_count >= count :
        lon = 0
        lat = 0
        for i in range(int(count)):
            lon += a[i][0] / count
            lat += a[i][1] / count
        print "final average " + str(lat) + ", " + str(lon)
        sys.exit()
    tlon = loc.longitude
    tlat = loc.latitude
    print str(curr_count) + " " + str(tlat) + ", " + str(tlon)
    a.append([])
    a[curr_count].append(tlon)
    a[curr_count].append(tlat)
    curr_count += 1

def main ():
    rospy.Subscriber("fix", NavSatFix, callback)
    rospy.init_node("GPS_AVG")
    rospy.spin()

if __name__ == '__main__':
    main()
