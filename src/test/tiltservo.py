# Moves a servo based on the accelerations of the Y axis

from Adafruit_I2C import Adafruit_I2C
from time import sleep
import Adafruit_BBIO.PWM as PWM


# initializes the i2c library and wakes up the IMU (MPU6050)
i2caddr = 0x68
i2c = Adafruit_I2C(i2caddr)
i2c.write8(0x6B, 0)

# sets up servo - from Adafruit tutorial
servoAddr = "P8_13"
duty_min = 3
duty_max = 14.5
duty_span = duty_max - duty_min

PWM.start(servoAddr, duty_max, 60.0)

# Utility funtion to convert a number in one range to another range
def map (x, min, max, newmin, newmax):
	x = x - min
	max = max - min
	x = x / max
	newspan = newmax - newmin
	x = x * newspan
	x = x + newmin
	return x

# for loop = laziness
for i in range (0, 10000):
	# reads in y axis accelerations and merges into one number
	b = i2c.readS8(0x3D)
	s = i2c.readU8(0x3E)
	rawaccel = b * 256 + s
	# converts raw reading into g's according to mode (+- 2 g's)
	g = rawaccel / 16384.
	# maps g's to the duty cycle range
	duty = map(g, -2, 2, duty_min, duty_max)
	# calls PWM & moves the servo
	PWM.set_duty_cycle(servoAddr, duty)

# cleanup time
PWM.stop(servoAddr)
PWM.cleanup()
i2c.write8(0x6B, 0x40)
