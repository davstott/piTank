# Take readings from the first channel of the PCF8591P I2C ADC

import smbus,time,datetime

class adc:
  def __init__(self):  
    self.i2c = smbus.SMBus(1)
    # The address in hex, look it up in i2cdetect -y 1 if you're unsure
    self.addr = 0x48
    # the maximum voltage we're expecting, as a float
    self.vMax = 3.3

  def dist2d120x(v):
    #todo: this in terms of 8bit ADC reading and fewer operators
    return (1.0 / (v / 15.69)) - 0.42

  def getValues(self, numberOfValues = 1, channel = 0):
    # returns values in volts
    if (channel >= 4):
      return None

    startTime = datetime.datetime.now()
    values = []
    
    # initialise the ADC
    #bits:
    #0, 1 = a/d channel number to read
    #2    = auto-increment flag (1 to enable)
    #3    = 0
    #4, 5 = configure inputs. 0 = 4 single ended inputs, 1 = 3 differential, 2 = mixed, 3 = two differential
    #6    = analogue output (1 to enable)
    #7    = 0
    
    #self.i2c.write_byte_data(self.addr, 0, channel)

    for i in range(numberOfValues):
      #read the value from register 0.
      #it's an 8bit ADC so we need to convert from 0-255 to 0-vMax
      #not quite sure why read_byte(addr) works and read_byte_data(addr, 0) doesn't
      value = self.vMax * self.i2c.read_byte(self.addr) / 255
      distance = dist2d120x(value)      
      elapsed = datetime.datetime.now() - startTime
      values.append({"elapsed": elapsed, "distance": distance})
      time.sleep(0.04) # 40ms snooze whilst it gets the next reading from the IR range sensor 

    return values

  def printValues(self, numberOfValues):
    print("time,value")
    values = self.getValues(numberOfValues)
    for value in values:
      print (str(value["elapsed"].seconds) + "." + str(value["elapsed"].microseconds) + "," + str(value["value"]))
