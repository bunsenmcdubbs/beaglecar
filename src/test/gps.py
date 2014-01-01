# code to test gps functionality
# code is from http://bradsmc.blogspot.com/2013/06/gps-for-beaglebone-black-d2523t-50.html
# need to try and install/use gpsd-clients library

import serial
import time
import datetime
import re
import os

os.system("echo uart1 > /sys/devices/bone_capemgr.9/slots")

serial = serial.Serial("/dev/ttyO1", baudrate=9600)

resp = ""

while True:
        while (serial.inWaiting() > 0):
                resp += serial.read()
                if "\r\n" in resp:
                        if "$GPRMC" in resp:
                                data = resp.split(',')
                                info = data[3] + " " + data[4] + " " + data[5] + " " + data[6]
                                print info
                        resp = ""

