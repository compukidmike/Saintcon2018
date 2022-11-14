# About the Badge
This year's badge features an ESP32 WiFi module running MicroPython. It has an 8x32 LED matrix display, 3 buttons, and 12 minibadge spots, as well as a rechargeable battery.
# Badge Instructions
## Building your badge
[BadgeBuildSheet.pdf](https://github.com/compukidmike/Saintcon2018/blob/master/Badge/BadgeBuildSheet.pdf) has instructions on how to assemble your badge
## Flashing your badge
You'll need some software to flash the code on your badge. 
The first thing you'll need is Python 3. This can be downloaded from https://www.python.org/downloads/
Once you have python installed, open a terminal/command prompt and run the following command: **pip install esptool**
You now have the tools you need to flash the code on your badge. Download **Saintcon2018.bin** from this github repository. 
Next, you will need to place the LOLIN D32 board into a mode where you can flash it's code.  To do this, you must pull GPIO pin 0 to ground.  This is best done by placing the LOLIN D32 board into a breadboard and pulling GPIO pin 0 to ground with a jumper wire.
Then, in a terminal window, navigate to the location of the badge firmware file, and run the following command, substituting the COM5 for the name of your badge serial port (this will vary depending on OS): **python esptool.py --port COM5 --baud 460800 write_flash --flash_size=detect 0 Saintcon2018.bin**

## Charging Your Badge
Simply use a microUSB cable to connect the badge to a USB power source (computer, phone charger, etc). This will power the badge as well as charge the battery.
The badge doesn't have an On/Off switch, so unplug the battery when you're not using it.

## Using Your Badge
The badge has 3 buttons labeled UP, DOWN, and SELECT. When first turned on, the badge is in display mode. Pressing the Up/Down buttons will cycle through the different displays. They are: SAINTCON, Custom Message, Hacker Challenge Score, Hacker Challenge ID.
 
Pressing Select will take you into the menu. The options here are: Brightness, Wifi Status, Wifi Config, Minibadges, Back. 
- Selecting Brightness will allow you to change the brightness of the LED matrix. 
- Selecting Wifi Status will show you if the wifi is connected or not. 
- Selecting Wifi Config will start the badge wifi configuration access point. In this mode, the display will show you the SSID and Password for the network that is being created by the badge. Connecting to that wifi network with your computer or phone will allow you to change badge settings like the wifi network that the badge connects to as well as the Custom Message. 
- Selecting Back will take you back to display mode.
 
Connecting your badge to a computer will allow you to do much more than the simple menu system allows, which brings us to...

## Editing Badge Code
To edit the badge code, I suggest an IDE called uPyCraft. It can be downloaded from http://docs.dfrobot.com/upycraft/ 
There are links on that page to tutorials on using the software.
One of the nice things about MicroPython is that the source code is all contained within the device, so you don't need to download the source to get started editing. uPyCraft can directly edit the files on the module.
