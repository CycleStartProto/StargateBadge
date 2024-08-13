# StargateBadge
A fun little limited run badge project
![2024-08-12 17 58 46](https://github.com/user-attachments/assets/fad5ef80-1e85-4c86-b748-a3f3511a8501)

see dropbox link for full repo including 3d files (too big for github): https://www.dropbox.com/s/36e33p1j47o0ms9/StargateBadge.zip?dl=0

# Known Issues
- 3d print gets really close to LEDs and can damage them during assembly, be VERY CAREFUL
  - Doing a light debur with a knife on the edges of the 3d print helps aleviate this issue
- Once a single LED is damaged it can cause large sections of the gate to stop working
  - Only fix is to rework the damaged LED.

# Mechanical Details
- Main structure is provided by the 3d printed core and the 2 circuit boards sandwitched together. 
- 3 pieces of 2x3 pin header hold the whole stack together through friction
- The infinity mirror is made from a 2.5mm thich fully silvered mirror, a piece of 2mm acrylic, and a 1mm 40% semi silvered mirror
- The infinity mirror stack is held in place with another 3d printed spacer to keep it in place and together


# Electrical Details
- 2000mAh Lipo Battery with TP4056 charge controller (set for 600mA charge rate) and power sharing circuit.
- Battery voltage measurement through 750k resistor (to prevent phantom-drain when powerd off) and op-amp buffer to microcontroller ADC
- MT3608 5V Boost converter circuit to ensure consistent LED Supply Voltage
- RP2040 Microcontroller with 128Mbit flash chip
- LIS3DHTR Accelerometer
- 74LVC4245APW Level shifter to ensure reliable addressable LED operation
- a total of 126 XL-1010RGBC-WS2812B 1mmx1mm addressable LEDs

# Firmware Details
- Adafruit Circuitpython and accompanying libraries for accelerometer and addressable LED's
- Custom animation parser for reading animations stored in plain-text format on flash (see command structure.txt in firmware folder for more info)
- Main settings stored as .txt file on flash (see BoardSettings.txt)
- Seperate USB-Serial endpoint exposed to accept animation commands
  - Same command structure as animation file
  - Will execute along side or on top of commanded animation file
  - Can be used to stream animations from seperate pc/controller
- 4 tactile buttons
  - UK1 (GP10) Dial outgoing wormhole
  - UK2 (GP11) Display battery voltage (will interrupt dial animations)
  - UK3 (GP12) Mode Select (switches between dial mode, accelerometer display mode, and rainbow mode)
  - UK4 (GP13) Incoming wormhole
- In random dial mode (default mode) gate will randomly dial an incoming or outgoing sequence based on randomization settings in BoardSettings.txt

# Animation Generators
- run on PC to quickly generate animation files to be loaded onto board
- Animation generators require python 3.9 or newer installed
- Run GenerateDialSeq.py to generate incoming, outgoing, idle, and close animation files
  - tweaking this generator is the easiset way to change relative brightnesses, chevron and glyph color, etc
- Run RainbowGen.py to generate rainbow animation
- Stargate mounts as USB flash drive, copy coresponding .anim files to root of circuitpython drive to load.
