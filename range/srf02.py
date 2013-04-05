# Take readings from the I2C SRF02 Ultrasound range sensor

import smbus,time,datetime

class srf02:
  def __init__(self):
    self.i2c = smbus.SMBus(1)
    # The address in hex, look it up in i2cdetect -y 1 if you're unsure
    self.addr = 0x70
  
  def getValues(self, numberOfValues):
    startTime = datetime.datetime.now()
    values = []

    for i in range(numberOfValues):
      self.i2c.write_byte_data(self.addr, 0, 81)
      time.sleep(0.08) # 80ms snooze whilst it pings
      #it must be possible to read all of these data in 1 i2c transaction
      #buf[0] software version. If this is 255, then the ping has not yet returned
      #buf[1] unused
      #buf[2] high byte range
      #buf[3] low byte range
      #buf[4] high byte minimum auto tuned range
      #buf[5] low byte minimum auto tuned range
      distance = self.i2c.read_word_data(self.addr, 2) / 255
      mindistance = self.i2c.read_word_data(self.addr, 4) / 255
      elapsed = datetime.datetime.now() - startTime
      values.append({"elapsed": elapsed, "distance": distance, "mindistance": mindistance}) 
      time.sleep(0.12) # 120ms snooze so we only take 5 readings per second

    return values

  def printValues(self, numberOfValues):
    print("time,range,minRange")
    values = self.getValues(numberOfValues)
    for value in values: 
      print (str(value["elapsed"].seconds) + "." + str(value["elapsed"].microseconds) + "," + str(value["distance"]) + "," + str(value["mindistance"]))
