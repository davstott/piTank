# Take readings from the first channel of the PCF8591P I2C ADC

import smbus,time,datetime
i2c = smbus.SMBus(1)
# The address in hex, look it up in i2cdetect -y 1 if you're unsure
addr = 0x48
# the maximum voltage we're expecting
vMax = 3.3

startTime = datetime.datetime.now()

print("time,value")

# initialise the ADC
#bits:
#0, 1 = a/d channel number to read
#2    = auto-increment flag (1 to enable)
#3    = 0
#4, 5 = configure inputs. 0 = 4 single ended inputs, 1 = 3 differential, 2 = mixed, 3 = two differential
#6    = analogue output (1 to enable)
#7    = 0

i2c.write_byte_data(addr, 0, 0)

for i in range(300):
  #read the value from register 0. it's an 8bit ADC so we need to convert from 0-255 to 0-vMax
  #not quite sure why read_byte(addr) works and read_byte_data(addr, 0) doesn't
  value = vMax * i2c.read_byte(addr) / 255
  elapsed = datetime.datetime.now() - startTime
  print (str(elapsed.seconds) + "." + str(elapsed.microseconds) + "," + str(value))
  time.sleep(0.04) # 40ms snooze whilst it gets the next reading from the IR range sensor
