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
| Example | 0xXX | PCA9536 |

