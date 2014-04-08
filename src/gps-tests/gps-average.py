#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
import simplekml

count = 300.
curr_count = 0
lon = 0.
lat = 0.

kml = simplekml.Kml()

def callback (loc):
    global curr_count
    global lon
    global lat
    if curr_count == count :
        print "final average " + str(lat) + ", " + str(lon)
        kml.newpoint(name="average", coords=[(lon, lat)])
        kml.save("gpsaverage.kml")
        curr_count += 1
        return
    elif curr_count > count :
        return
    tlon = loc.longitude
    tlat = loc.latitude
    kml.newpoint(name=str(curr_count), coords=[(tlon,tlat)])
    print str(curr_count) + " " + str(tlat) + ", " + str(tlon)
    lon += tlon / count
    lat += tlat / count
    curr_count += 1

def main ():
    rospy.Subscriber("fix", NavSatFix, callback)
    rospy.init_node("GPS_AVG")
    rospy.spin()

if __name__ == '__main__':
    main()
