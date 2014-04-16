BeagleCar
=========

Self driving car powered by the BeagleBone Black and a cheap RC car. Herein lay
 the brains, test-code, and other random development detritus involved in the 
making of my senior project.

Read about this project on my 
[website](http://andrewdai.co/beaglecar/intro.html)

Besides the short tests in `src/test/` everything is built on top of
[ROS](http://ros.org). `src/test` has scripts that were the building
blocks of the later nodes and ROS code (test or not); I learned most
of the core functionality of getting values from sensors or controlling
motors (aka using the Adafruit BBIO library) in the scripts there.

`src/gyro-tests` is a self contained test that used the gyroscope to 
control a servo's position and/or a motor's speed.

`src/joystick-tests` tests using a joystick (wired USB Xbox 360 controller)
to control motors and a servo (aka the car). It utilizes the `joy` ROS node.

`src/gps-tests` just averages the values parsed and published by the
`nmea-navsat-driver` node and writes them to a KML value.

This project utilizes Adafruit's BBIO Library and ROS nodes joy and nmea-navsat-driver.
