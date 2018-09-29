import IS31FL3730
from Font5x7 import Font5x7
import time

class Matrix:
  def __init__(self, i2c):
    self.i2c = i2c
    self.left = IS31FL3730.IS31FL3730(i2c, 0x60)
    self.right = IS31FL3730.IS31FL3730(i2c, 0x61)
    self.buffer = bytearray(32)
    
  def set_pixel(self, x, y, value):
    if value == 1:
      self.buffer[x] = self.buffer[x] | (1<<y)
    else:
      self.buffer[x] = self.buffer[x] & ~(1<<y)
    
  def set_pixel_async(self, x, y, value=1):
    set_pixel(x,y,value)
    update_display()
    
  def set_pixels(self, data):
    for x in range(32):
      self.buffer[x] = data[x]
  
  def update_display(self):
    data = bytearray(16)
    for x in range(16):
      data[x] = self.buffer[x]
    self.left.updateLEDs(data)
    for x in range(16):
      data[x] = self.buffer[x+16]
    self.right.updateLEDs(data)
    self.left.latchLEDs()
    self.right.latchLEDs()
    
  def brightness(self, value):
    self.left.brightness(value)
    self.right.brightness(value)
    
  def clear(self):
    for x in range(32):
      self.buffer[x] = 0
    
  def char(self, char, x):
    for i in range(5):
      if x+i < 32 and x+i >= 0:
        self.buffer[i+x] = Font5x7.font[ord(char)-32][i]
        self.buffer[i+x] = (((self.buffer[i+x] & 0x01)<<7) | ((self.buffer[i+x] & 0x02)<<5) | ((self.buffer[i+x] & 0x04)<<3) | ((self.buffer[i+x] & 0x08)<<1)
        | ((self.buffer[i+x] & 0x10)>>1) | ((self.buffer[i+x] & 0x20)>>3) | ((self.buffer[i+x] & 0x40)>>5) | ((self.buffer[i+x] & 0x80)>>7))
    
  def word(self, chars, x):
    counter = x
    self.clear()
    for i in chars:
      self.char(i, x)
      x += 6
        
      
  def transition(self, type, nextword):
    buffer2 = bytearray(32)
    buffer2[:] = self.buffer[:]
    self.word(nextword, 0)
    buffer3 = bytearray(32)
    buffer3[:] = self.buffer[:]
    self.clear()
    for y in range(11):
      for x in range(32):
        if(type == 1):
          self.buffer[x] = buffer2[x] << y+1 | (buffer3[x] >> 10-y)
        if(type == 2):
          self.buffer[x] = buffer3[x] << 10-y | (buffer2[x] >> y+1 )
      self.update_display()
      time.sleep_ms(20)
        
        
        
        
        




