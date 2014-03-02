#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM

# Author: Andrew Dai
# MIT License

# This class controls a servo by converting angles between 0 and 180
# into the proper frequency for servo PWM. It can also have maximum
# and minimum angles that clamp input angles.

class Servo:
    """Servo Controller defaults to pin8_13"""

    # Starts the servo controller with a PWM pin and initial angle.
    # Todo: set a GPIO pin to control on/off
    def __init__(self, pin = "P8_13", start_angle = 90):
        self.servo_pin = pin
        self.duty_max = 14.5
        self.duty_min = 3.
        self.duty_span = self.duty_max - self.duty_min
        self.upper_lim = 180.
        self.lower_lim = 0.
        self.running = False
        self.angle = 0.
        self.set_angle(start_angle)
        return
    
    # Still need to implement powering on
    def start(self):
        # Step 1: turn on 5v power line (will need to know GPIO pin)
        print "Starting the servo! Turn on the 5v line"
        # Step 2: start PWM
        PWM.start(self.servo_pin, self.angle, 60.0)
        # Step 3: set running flag to true
        self.running = True
        return
    
    # Still need to implement powering off
    def stop(self):
        print "Stopping the servo! Turn off the 5v line"
        PWM.stop(self.servo_pin)
        PWM.cleanup()
        self.running = False
        return

    # Prevents the angle from going beyond the upper and lower angle limits
    def clamp (self, angle):
        if angle < self.lower_lim: return self.lower_lim
        if angle > self.upper_lim: return self.upper_lim
        return angle

    # Sets the angle of the servo (clamped).
    # If the servo is not currently on (self.running == True) then only the
    # self.angle variable is changed. Otherwise the PWM duty cycle is also
    # changed.
    def set_angle(self, angle, clamp = True):
        if clamp: self.angle = float(self.clamp(angle))
        else: self.angle = float(angle)
        if self.running:
            duty = self.angle / 180. * self.duty_span + self.duty_min
            PWM.set_duty_cycle(self.servo_pin, duty)
        # print str(self.angle)
        return

def main():
    print "main method"
    servo = Servo()
    while True:
        input = raw_input("Enter and angle from 0 to 180. 'x' to exit:")
        if input == 'x':
            servo.stop()
            break
        servo.set_angle(input)

if __name__ == '__main__': main()
