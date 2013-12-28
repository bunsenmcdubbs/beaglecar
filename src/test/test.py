from Adafruit_I2C import Adafruit_I2C
from time import sleep

# initialize i2c connection to MPU6050
# i2c address is 0x68
i2c = Adafruit_I2C(0x68)

# wake up the device (out of sleep mode)
# bit 6 on register 0x6B set to 0
i2c.write16(0x6B, 0)

# read and print acceleration on x axis
# Most significant byte on 0x3b
# Least significant byte on 0x3c
# Combined to obtain raw acceleration data
for x in range(0, 20):
	# getting values from the registers
	b = i2c.readS8(0x3b)
	s = i2c.readU8(0x3c)
	print (str(b) + " " + str(s))
	# converting 2 8 bit words into a 16 bit
	# signed "raw" value
	raw = b * 255 + s
	print (raw)
	# still needs to be converted into G-forces
	sleep(0.2)
