# Code from Adafruit's Tutorials on Servo Usage with BBB
# Updated to work with the new PWM duty funtionality in the
# Adafruit_BBIO library

import Adafruit_BBIO.PWM as PWM
 
servo_pin = "P8_13"
duty_min = 3
duty_max = 14.5
duty_span = duty_max - duty_min
 
PWM.start(servo_pin, (duty_max), 60.0)
 
while True:
    angle = raw_input("Angle (0 to 180 x to exit):")
    if angle == 'x':
        PWM.stop(servo_pin)
        PWM.cleanup()
        break
    angle_f = float(angle)
    duty = ((angle_f / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(servo_pin, duty)
