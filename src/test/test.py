from Adafruit_I2C import Adafruit_I2C
from time import sleep

# initialize i2c connection to MPU6050
# i2c address is 0x68
i2c = Adafruit_I2C(0x68)

# wake up the device (out of sleep mode)
# bit 6 on register 0x6B set to 0
i2c.write8(0x6B, 0)

print("X axis accelerations (in g's)")

# read and print acceleration on x axis
# Most significant byte on 0x3b
# Least significant byte on 0x3c
# Combined to obtain raw acceleration data
for x in range(0, 5):
	# getting values from the registers
	b = i2c.readS8(0x3b)
	s = i2c.readU8(0x3c)
	# converting 2 8 bit words into a 16 bit
	# signed "raw" value
	raw = b * 256 + s
	# still needs to be converted into G-forces
	g = raw / 16384.
	print (str(g))
	sleep(0.2)
