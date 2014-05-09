#!/usr/bin/env python
import rospy, math
from geometry_msgs.msg import Pose2D, Vector3D
from servo_controller import Servo

p = 0.5
d = 0.0

#lastTurn = 0
#lastTime
target = Pose2D()

def setTarget(t):
  target = t
  return

def turn(angle = 0):
  # set angle on servo
  print angle
  return

def capturedTarget():
  print "Captured!!"
  return

# P controller
def steer(pose):
  
  # check for proximity to the target
  dx = target.x - pose.x
  dy = target.y - pose.y
  
  # if the car is inside a 2 meter radius of the target
  if math.pow(dx, 2) + math.pow(dy, 2) < 4:
    capturedTarget()
  
  global p, target
  current_heading = pose.theta
  desired_heading = math.arctan2( dy, dx )
  
  # p component
  pTurn = ( desired_heading - current_heading ) * p
  
  # d component - IMPLEMENT
  
  turn(pTurn)
  return
  
def main():
  rospy.Subscriber("loc", Pose2D, steer)
  rospy.spin()

if __name__ == "__main__":
  main()
