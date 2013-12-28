from Adafruit_I2C import Adafruit_I2C
from time import sleep

i2c = Adafruit_I2C(0x68)

i2c.write16(0x6B, 0)

for x in range(0, 20):
	b = i2c.readS8(0x3b)
	s = i2c.readU8(0x3c)
	print (str(b) + " " + str(s))
	sleep(0.2)
