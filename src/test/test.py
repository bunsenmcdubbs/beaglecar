from Adafruit_I2C import Adafruit_I2C
 
i2c = Adafruit_I2C(0x68)

i2c.write16(0x6B, 0)
print(i2c.readS8(0x3B))
