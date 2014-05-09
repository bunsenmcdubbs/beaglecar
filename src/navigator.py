#!/usr/bin/env python
import rospy, math
from geometry_msgs.msg import Pose2D, Vector3D

p = 0.5
d = 0.0

lastTurn = 0
target = Pose2D()

def setTarget(t):
  target = t

def turn(angle = 0):
  # set angle on servo

# PD controller
def steer(pose):
  
  # check for proximity to the target
  
  global lastTurn, p, d, target
  current_heading = pose.theta
  desired_heading = math.arctan2( target.y - pose.y, target.x - pose.x)
  
  # p component
  pTurn = ( desired_heading - current_heading ) * p
  
  # d component
  # TODO!!!
  dTurn = 0
  
  turn(angle = pTurn + dTurn)
  lastTurn = pTurn + dTurn

def main():
  rospy.Subscriber("loc", Pose2D, steer)

if __name__ == "__main__":
  main()
