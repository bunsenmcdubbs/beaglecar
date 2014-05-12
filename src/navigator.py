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

# set the current target to "t"
def setTarget(t):
  target = t
  return

# set angle on steering
def turn(angle = 0):
  car.turn(angle)
  return

# drove to the target!
# stop the car (speed = 0)
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
  # then we have "captured" the target
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
  # subscribes to the "loc" topic listening for Pose2D messages
  rospy.Subscriber("loc", Pose2D, steer)
  # start the car to drive at 30% speed
  car.set_speed(30)
  # listening
  rospy.spin()

if __name__ == "__main__":
  main()
