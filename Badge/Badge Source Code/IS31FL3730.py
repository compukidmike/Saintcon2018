
class IS31FL3730:
  def __init__(self, i2c, address=0x60):
    self.i2c = i2c
    self.address = address
    data = bytearray(2)
    data[0] = 0x0D #current limit regsister
    data[1] = 0x0C #20mA current limit
    self.i2c.writeto(self.address, data, True)
    data[0] = 0x00 #config regsister
    data[1] = 0x18 #set dual matrix mode
    self.i2c.writeto(self.address, data, True)
    
  def brightness(self, brightness):
    if brightness > 128: #max value is 128
      brightness = 128
    data = bytearray(2)
    data[0] = 0x19 #PWM regsister
    data[1] = brightness #0-128
    self.i2c.writeto(self.address, data, True)
    
  def updateLEDs(self, buffer):
    buff = bytearray(9)
    buff[0] = 0x01
    buff[1] = buffer[0]
    buff[2] = buffer[1]
    buff[3] = buffer[2]
    buff[4] = buffer[3]
    buff[5] = buffer[4]
    buff[6] = buffer[5]
    buff[7] = buffer[6]
    buff[8] = buffer[7]
    self.i2c.writeto(self.address, buff, True)
    buff[0] = 0x0E
    buff[1] = buffer[8]
    buff[2] = buffer[9]
    buff[3] = buffer[10]
    buff[4] = buffer[11]
    buff[5] = buffer[12]
    buff[6] = buffer[13]
    buff[7] = buffer[14]
    buff[8] = buffer[15]
    self.i2c.writeto(self.address, buff, True)
    
  def latchLEDs(self):
    data = bytearray(2)
    data[0] = 0x0C
    data[1] = 0x00
    self.i2c.writeto(self.address, data, True)
