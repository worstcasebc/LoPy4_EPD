# LoPy4-EPD
First project using micropython on Pycom LoPy4 together with an EPD. It's a demo-project for displaying text on an EPD.

## Overview
Transform .ttc to .ttf fonts online with https://transfonter.org/ttc-unpack
Convert .ttf font into python .py file or binary font file with https://github.com/peterhinch/micropython-font-to-py
I added a new function to the font-file to create a width-array for all contained characters. That is used by the text-wrapper to optimize the number of words shown per line.

### Hardware used
* [Pycom LoPy4](https://pycom.io/product/lopy4/) (LoRa-antenna is necessary to not destroy your board)
* [Pycom Expansion Board 2.0](https://pycom.io/product/expansion-board-3-0/)
* [Waveshare EPD](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT)
* a few jumper cables and a breadboard

### Wiring
|LoPy4          |Display        |Description                            |
| ------------- | ------------- | ------------------------------------- |
| 3.3V          | 3.3V          | the display is working with 3.3V      |
| GND           | GND           |                                       |
| P19  (G6)     | RST           |                                       |
| P20  (G7)     | DC            |                                       |
| P18  (G30)    | BUSY          |                                       |
| P4   (G11)    | CS            |                                       |
| P11  (G22)    | DIN           | SPI MOSI                              |
| P10  (G17)    | CLK           | SPI clock signal                      |

### Used libraries
Based on the Adafruit Framebuffer class an the Waveshare-EPD libraries I added new functionality to support Python-fonts with all display-rotations.

### Code
At the top of main.py select the used EPD and the rotation as well as the font. Own fonts can be created with the tools mentioned above. 