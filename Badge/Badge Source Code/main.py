#Saintcon2018 Badge Code
#by compukidmike and bashninja

#hardware platform: ESP32

import time
import machine
import matrix
import uasyncio as asyncio
from aswitch import Pushbutton

import configure
import wifi_config
import hc
import hcid as HCID

import _thread

hcid = HCID.getHCID()

hcidPassword = HCID.getPassword()

wifiConfigMode = 0
wifiMacAddr = HCID.getMac()
print("MAC Address: " + wifiMacAddr)
wifiConfigSSID = "SC_" + str(wifiMacAddr)[-5:-1]

ssid = ""


i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25), freq=100000)
i2c2 = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)

#Add minibadge I2C addresses to this list
I2CDeviceList = {0x01,0x29,0x40, 0x41, 0x42}
#I2CDeviceList = {0x01,0x40}
#Add minibadges with I2C EEPROMs to this list
I2CEEPROMList = {}

led = matrix.Matrix(i2c)
brightness = 32
displayUpdateDelay = 75
nextDisplayUpdateTime = 0
currentTicks = 0
animationCounter = 0

upPressed = 0
downPressed = 0
selectPressed = 0

displayState = 1
previousDisplayState = 1
displayMode = 0
currentAnimation = 0

userHandle = 'Test'
userHCScore = 0
userCustomMessage = 'Custom Message'

minibadgePreviousDisplayState = 0
minibadgeTextMessage = 'empty'
pixelDisplayData = bytearray(32)
pixelDisplayDelay = 2000


pwrEnable = machine.Pin(23, machine.Pin.OUT)
pwrEnable.value(1) #Turn on minbadge power

displayEnable = machine.Pin(27, machine.Pin.OUT)
displayEnable.value(1) #Enable matrix drivers

upPin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
downPin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
selectPin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

#set LED matrix brightness
led.brightness(brightness)

#Send brightness to all minibadges
data = bytearray(3)
for x in I2CDeviceList:
  if x != 0x01:
    try:
      i2c2.start()
      data[0] = x<<1 
      data[1] = 0x02
      data[2] = brightness
      i2c2.write(data)
      i2c2.stop()
    except:
      pass
#print(i2c2.scan()) #Use this to debug I2C stuff


async def buttonPressed(button): #up=1,down=2,select=3
  global displayState
  if displayState != 18 and displayState != 19:
    switcher = {
      1: stateSaintcon,
      2: stateCustom,
      3: stateHCScore,
      4: stateHCID,
      5: stateBroadcast,
      6: stateMenuBrightness,
      7: stateMenuHandleEdit,
      8: stateMenuWifiStatus,
      9: stateMenuWifiConfig,
      10: stateMenuMinibadges,
      12: stateMenuBack,
      13: stateBrightness,
      14: stateHandleEdit,
      15: stateWifiStatus,
      16: stateWifiConfig,
      17: stateMinibadges
    }
    func = switcher.get(displayState)
    result = func(button)
    #print("state:", displayState)
  
  
def stateSaintcon(button): #1
  global displayState
  global userCustomMessage
  if(button == 1): #Up Button
    userCustomMessage = wifi_config.get_custom_message()
    displayState = 4 #Custom
  if(button == 2): #Down Button
    displayState = 2 #Handle
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateCustom(button): #2
  global displayState
  if(button == 1): #Up Button
    displayState = 1 #Saintcon
  if(button == 2): #Down Button
    displayState = 3 #HCScore
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateHCScore(button): #3
  global displayState
  global userCustomMessage
  if(button == 1): #Up Button
    displayState = 2 #Handle
  if(button == 2): #Down Button
    userCustomMessage = wifi_config.get_custom_message()
    displayState = 4 #Custom
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateHCID(button): #4
  global displayState
  if(button == 1): #Up Button
    displayState = 3 #HCScore
  if(button == 2): #Down Button
    displayState = 1 #Saintcon
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateBroadcast(button): #5
  global displayState
  global userCustomMessage
  if(button == 1): #Up Button
    userCustomMessage = wifi_config.get_custom_message()
    displayState = 4 #Custom
  if(button == 2): #Down Button
    displayState = 2 #Handle
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateMenuBrightness(button): #6
  global displayState
  if(button == 1): #Up Button
    displayState = 12 #MenuBack
  if(button == 2): #Down Button
    displayState = 8 #MenuHandleEdit
  if(button == 3): #Select Button
    displayState = 13 #Brightness

def stateMenuHandleEdit(button): #7
  #not implemented
  return

def stateMenuWifiStatus(button): #8
  global displayState
  global ssid
  if(button == 1): #Up Button
    displayState = 6 #MenuHandleEdit
  if(button == 2): #Down Button
    displayState = 9 #MenuWifiConfig
  if(button == 3): #Select Button
    ssid = wifi_config.get_ssid()
    displayState = 15 #WifiStatus
    
def stateMenuWifiConfig(button): #9
  global displayState
  global wifiConfigMode
  if(button == 1): #Up Button
    displayState = 8 #MenuWifiStatus
  if(button == 2): #Down Button
    displayState = 10 #MenuMinibadges
  if(button == 3): #Select Button
    displayState = 16 #WifiConfig
    wifiConfigMode = 1
    
def stateMenuMinibadges(button): #10
  global displayState
  if(button == 1): #Up Button
    displayState = 9 #MenuWifiConfig
  if(button == 2): #Down Button
    displayState = 12 #MenuBrightness
  if(button == 3): #Select Button
    displayState = 17 #Minibadges
    
def stateMenuBack(button): #12
  global displayState
  if(button == 1): #Up Button
    displayState = 10 #MenuMinibadges
  if(button == 2): #Down Button
    displayState = 6 #MenuBrightness
  if(button == 3): #Select Button
    displayState = 1 #Saintcon
    
def stateBrightness(button): #13
  global displayState
  global brightness
  if(button == 1): #Up Button
    brightness += 10
    if(brightness > 128):
      brightness = 128
  if(button == 2): #Down Button
    brightness -= 10
    if(brightness < 1):
      brightness = 1
  led.brightness(brightness)
  data = bytearray(3)
  for x in I2CDeviceList:
    if x != 0x01:
      try:
        i2c2.start()
        data[0] = x<<1 
        data[1] = 0x02
        data[2] = brightness
        i2c2.write(data)
        i2c2.stop()
      except:
        pass
  if(button == 3): #Select Button
    displayState = 6 #MenuBrightness
    
def stateHandleEdit(button): #14
  #not implemented
  return
    
def stateWifiStatus(button): #15
  global displayState
  if(button == 3): #Select Button
    displayState = 8 #MenuWifiStatus
    
def stateWifiConfig(button): #16
  global displayState
  if(button == 1): #Up Button
    displayState = 16
  if(button == 2): #Down Button
    displayState = 16
  if(button == 3): #Select Button
    displayState = 16 #MenuWifiConfig

def stateMinibadges(button): #17
  global displayState
  global displayEnable
  if(button == 1): #Up Button
    if(pwrEnable.value() == 1):
      pwrEnable.value(0)
    else:
      pwrEnable.value(1)
  if(button == 2): #Down Button
    if(pwrEnable.value() == 1):
      pwrEnable.value(0)
    else:
      pwrEnable.value(1)
  if(button == 3): #Select Button
    displayState = 10 #MenuMinibadges
    

async def updateDisplay():
  global animationCounter
  global scrollCounter
  global displayUpdateDelay
  global displayState
  global previousDisplayState
  global userHandle
  global userHCScore
  global userCustomMessage
  global minibadgeTextMessage
  global minibadgePreviousDisplayState
  global pixelDisplayData
  global pixelDisplayDelay
  global ssid
  
  while(True):
    if(previousDisplayState != displayState):
      previousDisplayState = displayState
      animationCounter = 0
    
    if(displayState == 1): #Saintcon
      animationCounter += 1
      if(animationCounter > 80):
        animationCounter = 0
      led.word("SAINTCON",32-animationCounter)
      
    
    if(displayState == 2): #Custom
      if((len(str(userCustomMessage)) * 6)-1 > 32):
        animationCounter += 1
        if(animationCounter > (len(str(userCustomMessage)) * 6)+32):
          animationCounter = 0
        led.word(str(userCustomMessage),32-animationCounter)
      else:
        led.word(str(userCustomMessage), int((32-(len(str(userCustomMessage))*6))/2))
        

    if(displayState == 3): #HCScore
      if((len(str(userHCScore)) * 6)-1 > 32):
        animationCounter += 1
        if(animationCounter > (len(str(userHCScore)) * 6)+32):
          animationCounter = 0
        led.word(str(userHCScore),32-animationCounter)
      else:
        led.word(str(userHCScore), int((32-(len(str(userHCScore))*6))/2))
        
    if(displayState == 4): #HCID
      message = "HCID: " + hcid
      if((len(message) * 6)-1 > 32):
        animationCounter += 1
        if(animationCounter > (len(message) * 6)+32):
          animationCounter = 0
        led.word(message,32-animationCounter)
      else:
        led.word(message, int((32-(len(message)*6))/2))
    
    #if(displayState == 5): #Broadcast
      #do something

    
    if(displayState == 6): #MenuBrightness
      animationCounter += 1
      if(animationCounter > (len("BRIGHTNESS") * 6)+32):
        animationCounter = 0
      led.word("BRIGHTNESS",32-animationCounter)
    
    if(displayState == 7): #MenuHandleEdit
      animationCounter += 1
      if(animationCounter > (len("HANDLE EDIT") * 6)+32):
        animationCounter = 0
      led.word("HANDLE EDIT",32-animationCounter)
    
    if(displayState == 8): #MenuWifiStatus
      animationCounter += 1
      if(animationCounter > (len("WIFI STATUS") * 6)+32):
        animationCounter = 0
      led.word("WIFI STATUS",32-animationCounter)
    
    if(displayState == 9): #MenuWifiConfig
      animationCounter += 1
      if(animationCounter > (len("WIFI CONFIG") * 6)+32):
        animationCounter = 0
      led.word("WIFI CONFIG",32-animationCounter)
    
    if(displayState == 10): #MenuMinibadges
      animationCounter += 1
      if(animationCounter > (len("MINIBADGES") * 6)+32):
        animationCounter = 0
      led.word("MINIBADGES",32-animationCounter)
    
    if(displayState == 12): #MenuBack
      animationCounter += 1
      if(animationCounter > (len("BACK") * 6)+32):
        animationCounter = 0
      led.word("BACK",32-animationCounter)
    
    if(displayState == 13): #Brightness
      global brightness
      led.word(str(brightness), int((32-(len(str(brightness))*6))/2))
    
    if(displayState == 14): #HandleEdit
      #not implemented
      return
    
    if(displayState == 15): #WifiStatus
      animationCounter += 1
      if wifi_config.is_wifi_connected():
        message = "CONNECTED TO: " + ssid + " IP: " + wifi_config.get_device_ip()
      else:
        message = "NOT CONNECTED"
      if(animationCounter > (len(message) * 6)+32):
        animationCounter = 0
      led.word(message,32-animationCounter)
    
    if(displayState == 16): #WifiConfig
      animationCounter += 1
      message = "SSID: " + wifiConfigSSID + " PASS: " + hcidPassword
      if(animationCounter > (len(message) * 6)+32):
        animationCounter = 0
      led.word(message,32-animationCounter)
    
    if(displayState == 17): #Minibadges
      if(pwrEnable.value() == 1):
        led.word("ON", int((32-(len("ON")*6))/2))
      else:
        led.word("OFF", int((32-(len("OFF")*6))/2))
    
    if(displayState == 18): #Minibadge Text Message
      animationCounter += 1
      if((len(minibadgeTextMessage) * 6)-1 > 32):
        
        if(animationCounter > (len(minibadgeTextMessage) * 6)+32):
          #animationCounter = 0
          displayState = minibadgePreviousDisplayState #put display back to where it was
        led.word(minibadgeTextMessage,32-animationCounter)
      else:
        if(animationCounter > 26): #(2000/displayUpdateDelay)):
          displayState = minibadgePreviousDisplayState #put display back to where it was
        led.word(minibadgeTextMessage, int((32-(len(minibadgeTextMessage)*6))/2))
    
    if(displayState == 19): #Minibadge Pixel Message
      animationCounter += 1
      if(animationCounter > (pixelDisplayDelay/displayUpdateDelay)):
        displayState = minibadgePreviousDisplayState
      led.set_pixels(pixelDisplayData)
      
    led.update_display()
    if pixelDisplayDelay > 0:
      await asyncio.sleep_ms(pixelDisplayDelay)
    else:
      await asyncio.sleep_ms(displayUpdateDelay)

async def minibadgeComms(): #Handle minibadge I2C communications
  global displayState
  global minibadgeTextMessage
  global minibadgePreviousDisplayState
  global pixelDisplayData
  global pixelDisplayDelay
  
  while(True):
    if displayState != 18 and displayState != 19:
      data = bytearray(1)
      pixelDisplayDelay = 0
      for x in I2CDeviceList:
        try:
          i2c2.start()
          data[0] = x<<1 | 0x1
          i2c2.write(data)
          i2c2.readinto(data, False)
          if data[0] == 1:
            data2 = bytearray(1)
            i2c2.readinto(data2, True) #get button status
          elif data[0] == 2: #Text Message
            i2c2.readinto(data, False) #get message length
            data2 = bytearray(data[0])
            i2c2.readinto(data2, True)
            minibadgePreviousDisplayState = displayState
            minibadgeTextMessage = str(data2)
            txtLength = len(minibadgeTextMessage)
            minibadgeTextMessage = minibadgeTextMessage[12:txtLength-2] #trim to just the message
            displayState = 18 #Minibadge Text Message
          elif data[0] == 3: #Pixel Message
            data2 = bytearray(32)
            i2c2.readinto(data2, True)
            minibadgePreviousDisplayState = displayState
            for x in range(32):
              pixelDisplayData[x] = data2[x]
            pixelDisplayDelay = 2000 #2 seconds
            displayState = 19 #Minibadge Pixel Message
          elif data[0] == 4: #Pixel Message with display time
            i2c2.readinto(data, False) #get display time
            pixelDisplayDelay = data[0] * 10
            data2 = bytearray(32)
            i2c2.readinto(data2, True)
            minibadgePreviousDisplayState = displayState
            for x in range(32):
              pixelDisplayData[x] = data2[x]
            displayState = 19 #Minibadge Pixel Message
          elif data[0] == 5: #Custom Message
            i2c2.readinto(data, False) #get message length
            data2 = bytearray(data[0])
            i2c2.readinto(data2, True)
          else:
            i2c2.readinto(data, True)
          i2c2.stop()
        except Exception as e:
          print(e)
        await asyncio.sleep_ms(1)
    if pixelDisplayDelay > 0:
      await asyncio.sleep_ms(pixelDisplayDelay)
    else:
      await asyncio.sleep_ms(100)
      
async def updateHCScore():
  while(True):
    userHCScore = hc.get_score(hcid)
    if userHCScore == "Error":
      userHCScore = "0"
    
    data = bytearray(4)
    for x in I2CDeviceList: #Send HC score to minibadges
      if x != 0x01:
        try:
          i2c2.start()
          data[0] = x<<1 
          data[1] = 0x01
          data[2] = userHCScore >> 8
          data[3] = userHCScore
          i2c2.write(data)
          i2c2.stop()
        except:
          pass
    
    await asyncio.sleep(60)

upBtn = Pushbutton(upPin)
downBtn = Pushbutton(downPin)
selectBtn = Pushbutton(selectPin)

upBtn.press_func(buttonPressed, (1,))
downBtn.press_func(buttonPressed, (2,))
selectBtn.press_func(buttonPressed, (3,))
upBtn.debounce_ms = 100


def startWifi():
  global userHCScore
  wifi_config.start_wifi()
  
  if wifi_config.is_wifi_connected():
    userHCScore = hc.get_score(hcid)
    if userHCScore == "Error":
      userHCScore = "0"
    print("-- H -- A -- C -- K -- E -- R -- M -- A -- N --")
    print("Hacker Score: " + str(userHCScore))
    print("Generated HCID: " + hcid)
    print("-- H -- A -- C -- K -- E -- R -- M -- A -- N --")

  
def configureWifi():
    authmode = 4 # wpa2
    configure.start_wifi_config(wifiConfigSSID, hcidPassword, authmode)
    wifi_config.start_wifi()
    

def start_loop():
  loop = asyncio.get_event_loop()
  loop.call_soon(updateDisplay())
  loop.call_soon(minibadgeComms())
  loop.call_soon(updateHCScore())
  loop.run_forever()

_thread.start_new_thread(start_loop, ())

startWifi()

while 1:
  if wifiConfigMode == 1:
      configureWifi()
      wifiConfigMode = 0
      displayState = 9


