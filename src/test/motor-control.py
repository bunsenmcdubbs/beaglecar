#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM

servo_pin = "P8_13"

PWM.start(servo_pin, 50, 50)

while True:
    duty = raw_input("Speed (0 to 100 x to exit):")
    if duty == 'x':
        PWM.stop(servo_pin)
        PWM.cleanup()
        break 
    PWM.set_duty_cycle(servo_pin, float(duty))
