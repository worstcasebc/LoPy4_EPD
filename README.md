# LoPy4-EPD
First project using micropython on Pycom LoPy4 together with an EPD 

## Overview


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
Adafruit framebuf and Waveshare Python-libs adapted for Micropython

### Code
The Lopy4 board connects to a WiFi first. This happens in the boot.py, that is called first after a start/reboot. You need to provide a SSID and the key for that WiFi within config.py. After WiFi is connected, the actual time is requested and stored to the RTC of the board.

