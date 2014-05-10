#!/usr/bin/env python
import rospy, math
from geometry_msgs.msg import Pose2D, Vector3D
from drive import Car

p = 0.5
#d = 0.0
#i = 0.05

#cumError = 0
#lastTurn = 0
#lastTime
target = Pose2D()

car = Car()

def setTarget(t):
  target = t
  return

def turn(angle = 0):
  # set angle on steering
  car.turn(angle)
  return

def capturedTarget():
  print "Captured!!"
  car.set_speed(0)
  # next target?
  return

# P controller
def steer(pose):

  # check for proximity to the target
  dx = target.x - pose.x
  dy = target.y - pose.y

  # if the car is inside a 1.5 meter radius of the target
  if math.pow(dx, 2) + math.pow(dy, 2) < 2.25:
    capturedTarget()

  global p, target
  current_heading = pose.theta
  desired_heading = math.arctan2( dy, dx )

  # p component
  pTurn = ( desired_heading - current_heading ) * p

  turn(pTurn)
  return

def main():
  rospy.Subscriber("loc", Pose2D, steer)
  car.set_speed(30)
  rospy.spin()

if __name__ == "__main__":
  main()
