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
* adc.py
  My python implementation of reading values in Volts from the I2C PCF8591P Analogue to Digital Converter IC. It also reports values in cm from the output of a Sharp 2D120X Infrared range sensor based upon an approximate calibration. Linearisation taken from the Sharp Datasheet, the regression is my own approximation.
* irCalibration.txt
  My readings in volts against distance in cm from the 2D120X sensor, including maximum and minimum sensed values at each point.
* irGraph.py
  Small script to help me eyeball the maths to convert ADC value into range.


(https://raw.github.com/davstott/piTank/master/range/lcdSonarGraph.png)



