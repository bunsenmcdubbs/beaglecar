#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM

class Servo:
    """Servo Controller defaults to pin8_13"""

    def __init__(self, pin = "P8_13", start_angle = 90):
        self.servo_pin = pin
        self.duty_max = 14.5
        self.duty_min = 3.
        self.duty_span = self.duty_max - self.duty_min
        self.upper_lim = 180.
        self.lower_lim = 0.
        self.running = False
        self.set_angle(start_angle)
        return

    def start(self):
        print "Starting the servo! Turn on the 5v line"
        PWM.start(servo_pin, duty_max / 2., 60.0)
        self.running = True
        return

    def stop(self):
        print "Stopping the servo! Turn off the 5v line"
        PWM.stop(servo_pin)
        PWM.cleanup()
        self.running = False
        return

    def clamp (self, angle):
        if angle < self.lower_lim: return self.lower_lim
        if angle > self.upper_lim: return self.upper_lim
        return angle

    def set_angle(self, angle):
        self.angle = float(self.clamp(angle))
        if self.running:
            duty = self.angle / 180. * self.duty_span + self.duty_min
            PWM.set_duty_cycle(servo_pin, duty)
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
