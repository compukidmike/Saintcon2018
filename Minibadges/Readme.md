# Minibadges
The minbadge spec is here, along with eagle and kicad footprints: https://github.com/lukejenkins/minibadge  

Notes:
- 5V may not be exactly 5V. It'll probably be battery voltage (3.7-4.2V).  
- SPI *might* be connected, but don't plan on it. It gets complicated with more minibadges (one CS line per badge).  
- Please be conservative with power consumption on your minibadge. There will be a lot more minibadge spots on the badge this year, so battery life is a concern.  

If you have questions, contact me (compukidmike on twitter/slack/gmail)

## I2C Addresses
To avoid conflicts, here is the list of known minibadge I2C addresses.
To get your minibadge on this list, submit a pull request or send me a message (compukidmike on twitter/slack/gmail)
The Chip column is so I know which I2C chips to support in the main badge code (no promises, but I'm going to try to add support for as many as I can). If you're using a microcontroller, send me a spec on what I2C commands to send to it.

| Minibadge Name | Address | Chip |
| --- | --- | --- |
| hakinthebox.com | 0x01 | ATTiny |
| TBA | 0x29 | ATTiny |
| Professor Plum | 0x41 | ATTiny |
| TBA | 0x42 | ATTiny |
| TBA | 0x51 | M24C01 |
| TBA | 0x52 | M24C01 |
| bashNinja | 0x53 | M24C01 |
| TBA | 0x54 | M24C01 |

## I2C Message Protocol
This is a preliminary message protocol for minibadges. You are more than welcome to come up with other means of communication and write the supporting code for the main badge. This is just a starting point... if you have ideas on expanding this, please contact me.  

Since there isn’t an Interrupt line for the minibadges, the badge will poll each minibadge for a status byte (if supported by the minibadge).

Polling Message: 
- Will occur at regular intervals (multiple times per second) 
- Badge will send a standard read message (address with R/W bit set to R) 
- The byte that is returned by the minibadge will determine what happens next 
   - If byte is 0x00, status is empty, badge will end communication 
   - If byte is 0x01, status is Button Pressed (or similar input) (NOTE: this just passes button state to the badge. You'll have to write some code to do something with that data)
      - Next byte is button status (limited to 1 byte or 8 buttons)
   - If byte is 0x02, status is Text Message (for display on badge) (will be displayed for as long as it takes to scroll across the dislpay)
      - Next byte is text length (max 255 characters)
      - Next bytes are ASCII text
   - If byte is 0x03, status is Pixel Message (for display on badge)  (will be displayed for 2 seconds)
      - Next 32 bytes are display columns (Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top)
   - If byte is 0x04, status is Pixel Message with display time (this enables some animations) (for display on badge)
      - Next byte is time to display message (range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments). This will also be the amount of time before the badge polls the minibadge again for the next animation frame
      - Next 32 bytes are display columns (Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top)
   - If byte is 0x05, status is Custom Data (this allows your minibadge to send custom data to the badge that will require writing code for the badge to do something with it)
      - Next byte is length of data in bytes
      - Next bytes are custom data

Badge Event Message: 
- Will be sent to minibadges when they occur
- 0x01 - HC Score Updated
   - Next bytes(2) is score (16bit value, max score of 65535) 
- 0x02 - Brightness Change (will also be sent after power on) 
   - Next byte is brightness value (0-128) (Yes, 128. I know it's strange, but that's the brightness range for the LED matrix driver.)
