# Take readings from the I2C SRF02 Ultrasound range sensor

import smbus,time,datetime
i2c = smbus.SMBus(1)
# The address in hex, look it up in i2cdetect -y 1 if you're unsure
srf = 0x70

startTime = datetime.datetime.now()

print("time,range,minRange")

for i in range(30):
  i2c.write_byte_data(srf, 0, 81)
  time.sleep(0.08) # 80ms snooze whilst it pings
  #it must be possible to read all of these data in 1 i2c transaction
  #buf[0] software version. If this is 255, then the ping has not yet returned
  #buf[1] unused
  #buf[2] high byte range
  #buf[3] low byte range
  #buf[4] high byte minimum auto tuned range
  #buf[5] low byte minimum auto tuned range
  distance = i2c.read_word_data(srf, 2) / 255
  mindistance = i2c.read_word_data(srf, 4) / 255
  elapsed = datetime.datetime.now() - startTime
  print (str(elapsed.seconds) + "." + str(elapsed.microseconds) + "," + str(distance) + "," + str(mindistance))
