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
| compukidmike | 0x40 | ATTiny |
| Professor Plum | 0x41 | ATTiny |
| TBA | 0x42 | ATTiny |
| TBA | 0x51 | M24C01 |
| TBA | 0x52 | M24C01 |
| bashNinja | 0x53 | M24C01 |
| TBA | 0x54 | M24C01 |

## I2C Message Protocol
This is a preliminary message protocol for minibadges. You are more than welcome to come up with other means of communication and write the supporting code for the main badge. This is just a starting point... if you have ideas on expanding this, please contact me.  

### Organization of I2C Messages

- The first byte of a polling response message is the status bytes.
- The first byte of an event message is the event type byte.
- These messages are organized (by this first byte) into address spaces according to their purpose.

| Range | Purpose | Description |
| --- | --- | --- |
| 0x00 - 0x3f | Badge/Minibadge | Messages between the badge and a minibadge |
| 0x40 - 0x7f | Minibadge/Minibadge | Messages from one minibadge to another (relayed by the badge) |
| 0x80 - 0xbf | Minibadge Broadcast | Messages from one minibadge to all others (relayed by the badge) |
| 0xc0 - 0xff | TBD | |


### Polling Message

Since there isn’t an Interrupt line for the minibadges, the badge will poll each minibadge for a status byte (if supported by the minibadge). This polling message:

- Will occur at regular intervals (multiple times per second) 
- Badge will send a standard read message (address with R/W bit set to R) 
- The byte that is returned by the minibadge will determine what happens next 

#### Polling Message Responses

| Status Byte | Status | Introduced |
| --- | --- | --- |
| 0x00 | None | 2018 |
| 0x01 | [to badge] Button Pressed | 2018 |
| 0x02 | [to badge] Text Message | 2018 |
| 0x03 | [to badge] Pixel Message | 2018 |
| 0x04 | [to badge] Pixel Animation Frame | 2018 |
| 0x05 | [to badge] Custom Data | 2018 |
| 0x41 | [to minibadge] Button Pressed | 2020 |
| 0x42 | [to minibadge] Text Message | 2020 |
| 0x43 | [to minibadge] Pixel Message | 2020 |
| 0x44 | [to minibadge] Pixel Animation Frame | 2020 |
| 0x45 | [to minibadge] Custom Data | 2020 |
| 0x81 | [broadcast] Button Pressed | 2020 |
| 0x82 | [broadcast] Text Message | 2020 |
| 0x83 | [broadcast] Pixel Message | 2020 |
| 0x84 | [broadcast] Pixel Animation Frame | 2020 |
| 0x85 | [broadcast] Custom Data | 2020 |

#### None

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x00 |

   - Badge will end communication.

#### [to badge] Button Pressed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x01 |
| 2 | Buttons | | limited to 1 byte or 8 buttons |

   - This just passes `Buttons` state to the badge. Badge code will have to be written to do something with that data.

#### [to badge] Text Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x02 |
| 2 | Text Length | | max 255 characters |
| 3-end | ASCII Text | | |

   - Badge will display `ASCII Text` for as long as it takes to scroll across the display

#### [to badge] Pixel Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x03 |
| 2-33 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will display `Display Columns` for 2 seconds

#### [to badge] Pixel Animation Frame

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x04 |
| 2 | Frame Duration | | Range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments. This will also be the amount of time before the badge polls the minibadge again for the next animation frame. |
| 3-34 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will display `Display Columns` for `Frame Duration` centiseconds.
   - Badge will then poll minibadge for the next frame.

#### [to badge] Custom Data

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x05 |
| 2 | Data Length | | max 255 bytes |
| 3 - end | Custom Data | | |

   - This allows your minibadge to pass `Custom Data` to the badge. Badge code will have to be written to do something with that data.

#### [to minibadge] Button Pressed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x41 |
| 2 | Recipient | | Minibadge address that badge should relay to |
| 3 | Buttons | | limited to 1 byte or 8 buttons |

   - Badge will raise `[from minibadge] Button Pressed` event to minibadge at `Recipient` address.

#### [to minibadge] Text Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x42 |
| 2 | Recipient | | Minibadge address that badge should relay to |
| 3 | Text Length | | max 255 characters |
| 4-end | ASCII Text | | |

   - Badge will raise `[from minibadge] Text Message` event to minibadge at `Recipient` address.

#### [to minibadge] Pixel Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x43 |
| 2 | Recipient | | Minibadge address that badge should relay to |
| 3-34 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will raise `[from minibadge] Pixel Message` event to minibadge at `Recipient` address.

#### [to minibadge] Pixel Animation Frame

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x44 |
| 2 | Recipient | | Minibadge address that badge should relay to |
| 3 | Frame Duration | | Range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments. This will also be the amount of time before the badge polls the minibadge again for the next animation frame. |
| 4-35 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will raise `[from minibadge] Pixel Animation Frame` event to minibadge at `Recipient` address.
   - Badge will then poll minibadge for the next frame.

#### [to minibadge] Custom Data

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x45 |
| 2 | Recipient | | Minibadge address that badge should relay to |
| 3 | Data Length | | max 255 bytes |
| 4 - end | Custom Data | | |

   - Badge will raise `[from minibadge] Custom Data` event to minibadge at `Recipient` address.

#### [broadcast] Button Pressed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x81 |
| 2 | Buttons | | limited to 1 byte or 8 buttons |

   - Badge will raise `[broadcast] Button Pressed` event to minibadges at all addresses.

#### [broadcast] Text Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x82 |
| 2 | Text Length | | max 255 characters |
| 3-end | ASCII Text | | |

   - Badge will raise `[broadcast] Text Message` event to minibadges at all addresses.

#### [broadcast] Pixel Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x83 |
| 2-33 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will raise `[broadcast] Pixel Message` event to minibadges at all addresses.

#### [broadcast] Pixel Animation Frame

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x84 |
| 2 | Frame Duration | | Range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments. This will also be the amount of time before the badge polls the minibadge again for the next animation frame. |
| 3-34 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Badge will raise `[broadcast] Pixel Animation Frame` event to minibadges at all addresses.
   - Badge will then poll minibadge for the next frame.

#### [broadcast] Custom Data

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x85 |
| 2 | Data Length | | max 255 bytes |
| 3 - end | Custom Data | | |

   - Badge will raise `[broadcast] Custom Data` event to minibadges at all addresses.

### Event Messages

- Will be sent to minibadges when they occur

| Type Byte | Type | Introduced |
| --- | --- | --- |
| 0x01 | [from badge] HC Score Updated | 2018 |
| 0x02 | [from badge] Brightness Changed | 2018 |
| 0x41 | [from minibadge] Button Pressed | 2020 |
| 0x42 | [from minibadge] Text Message | 2020 |
| 0x43 | [from minibadge] Pixel Message | 2020 |
| 0x44 | [from minibadge] Pixel Animation Frame | 2020 |
| 0x45 | [from minibadge] Custom Data | 2020 |
| 0x81 | [broadcast] Button Pressed | 2020 |
| 0x82 | [broadcast] Text Message | 2020 |
| 0x83 | [broadcast] Pixel Message | 2020 |
| 0x84 | [broadcast] Pixel Animation Frame | 2020 |
| 0x85 | [broadcast] Custom Data | 2020 |

#### [from badge] HC Score Updated

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Type | 0x01 |
| 2-3 | Score | 0-65535 | 16bit value, max score of 65535 |

#### [from badge] Brightness Changed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Type | 0x02 |
| 2 | Brightness | 0-128 | Yes, 128. I know it's strange, but that's the brightness range for the LED matrix driver. |

#### [from minibadge] Button Pressed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Type | 0x41 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Buttons | | limited to 1 byte or 8 buttons |

   - Minibadge at address `Sender` sent `[to minibadge] Button Pressed`, identifying this minbadge as the `Recipient`.

#### [from minibadge] Text Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x42 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Text Length | | max 255 characters |
| 4-end | ASCII Text | | |

   - Minibadge at address `Sender` sent `[to minibadge] Text Message`, identifying this minbadge as the `Recipient`.

#### [from minibadge] Pixel Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x43 |
| 2 | Sender | | Minibadge address that authored this message |
| 3-34 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Minibadge at address `Sender` sent `[to minibadge] Pixel Message`, identifying this minbadge as the `Recipient`.

#### [from minibadge] Pixel Animation Frame

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x44 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Frame Duration | | Range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments. This will also be the amount of time before the badge polls the minibadge again for the next animation frame. |
| 4-35 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Minibadge at address `Sender` sent `[to minibadge] Pixel Animation Frame`, identifying this minbadge as the `Recipient`.
   - Badge will poll `Sender` for another frame. Another event might result.

#### [from minibadge] Custom Data

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x45 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Data Length | | max 255 bytes |
| 4 - end | Custom Data | | |

   - Minibadge at address `Sender` sent `[to minibadge] Custom Data`, identifying this minbadge as the `Recipient`.

#### [broadcast] Button Pressed

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Type | 0x81 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Buttons | | limited to 1 byte or 8 buttons |

   - Minibadge at address `Sender` sent `[broadcast] Button Pressed`.

#### [broadcast] Text Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x82 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Text Length | | max 255 characters |
| 4-end | ASCII Text | | |

   - Minibadge at address `Sender` sent `[broadcast] Text Message`.

#### [broadcast] Pixel Message

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x83 |
| 2 | Sender | | Minibadge address that authored this message |
| 3-34 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Minibadge at address `Sender` sent `[broadcast] Pixel Message`.

#### [broadcast] Pixel Animation Frame

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x84 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Frame Duration | | Range is 0-255 x10 milliseconds, or 0-2.55 seconds in 10 millisecond increments. This will also be the amount of time before the badge polls the minibadge again for the next animation frame. |
| 4-35 | Display Columns | | Display is 8x32 pixels. 0,0 is bottom left corner. So first byte will fill the first column from bottom to top. |

   - Minibadge at address `Sender` sent `[broadcast] Pixel Animation Frame`.
   - Badge will poll `Sender` for another frame. Another event might result.

#### [broadcast] Custom Data

| Byte | Purpose | Value | Description |
| --- | --- | --- | --- |
| 1 | Status | 0x85 |
| 2 | Sender | | Minibadge address that authored this message |
| 3 | Data Length | | max 255 bytes |
| 4 - end | Custom Data | | |

   - Minibadge at address `Sender` sent `[to minibadge] Custom Data`.

