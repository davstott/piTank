I2C range sensing code
======================

* rpi_srf02.c
  Started out with the demonstration code to read from the SRF02 sensor using I2C from www.robot-electronics.co.uk/files/rpi_srf02.c and added a loop, minimum range reporting and logging the results to a text file.
* srf02.py
  My python implementation of reading multiple values for range and minimum range from the SRF02 over I2C. Implemented as a simple class so that it can be called by
* calibrate.py
  Added some basic statistics calculation and some user input, which logs some values to a text file which can be used to draw a calibration graph with error bars
* srf02Calibration.txt
  Example output from above
* lcdGraph.py
  Python script that takes single readings from srf02.py and uses pygame to display the result on a framebuffer display, such as an SPI LCD. It also uses matplotlib to draw a chart of the values, so it's an illustration of one way of combining the two libraries.

(https://raw.github.com/davstott/piTank/master/range/lcdSonarGraph.png)



