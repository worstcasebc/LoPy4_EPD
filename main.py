import time
import pycom
import config
import adafruit_framebuf
from machine import SPI

EPD_HEIGHT  = 176
EPD_WIDTH   = 264

if config.epd_type == "epd2in7":
    # Setting for 2in7 display
    from waveshare_epd import epd2in7
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    epd = epd2in7.EPD()
elif config.epd_type == "epd4in2":
    # Setting for 4in2 display
    from waveshare_epd import epd4in2
    EPD_WIDTH       = 400
    EPD_HEIGHT      = 300
    epd = epd4in2.EPD()
elif (config.epd_type == "epd7in5bc_color") or (config.epd_type == "epd7in5bc_bw"):
    # Setting for 7in5 display
    from waveshare_epd import epd7in5bc
    EPD_WIDTH       = 640
    EPD_HEIGHT      = 384
    epd = epd7in5bc.EPD()
else:
    print("Please set a display-type within config.py")

try:
    epd.init()

    bab = bytearray(EPD_WIDTH * EPD_HEIGHT // 8)
    for i in range(len(bab)):
        bab[i] = 0xFF
    fb = adafruit_framebuf.FrameBuffer(bab, EPD_WIDTH, EPD_HEIGHT, buf_format=adafruit_framebuf.MHMSB)
    fb.rotation = config.epd_rotation

    if (config.epd_type == "epd7in5bc_color") or (config.epd_type == "epd7in5bc_bw"):
        bay = bytearray(EPD_WIDTH * EPD_HEIGHT // 8)
        for i in range(len(bay)):
            bay[i] = 0xFF
        fb_red = adafruit_framebuf.FrameBuffer(bay, EPD_WIDTH, EPD_HEIGHT, buf_format=adafruit_framebuf.MHMSB)
        fb_red.rotation = config.epd_rotation

    if config.epd_rotation in (1, 3):
        tmp_width = EPD_WIDTH
        EPD_WIDTH = EPD_HEIGHT
        EPD_HEIGHT = tmp_width

    fb.circle(int(EPD_WIDTH / 2.5), int(EPD_HEIGHT / 2.5), 50, 0)
    fb.text('ABCDEFGHIJKLMNOP', 0, 0, 0)
    fb.text('BCDEFGHIJKLMNOP', 0, 8, 0)
    fb.text('CDEFGHIJKLMNOP', 0, 16, 0)
    fb.text('DEFGHIJKLMNOP', 0, 24, 0)
    fb.text('EFGHIJKLMNOP', 0, 32, 0)
    fb.text('FGHIJKLMNOP', 0, 40, 0)
    fb.text('GHIJKLMNOP', 0, 48, 0)
    fb.text('HIJKLMNOP', 0, 56, 0)
    fb.text('IJKLMNOP', 0, 64, 0)
    fb.text('JKLMNOP', 0, 72, 0)
    fb.text('KLMNOP', 0, 80, 0)
    fb.text('LMNOP', 0, 88, 0)

    if config.epd_type == "epd7in5bc_color":
        fb_red.rect(10, 10, EPD_WIDTH - 20, EPD_HEIGHT - 20, 0)
        fb_red.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf, fb_red.buf)
    elif config.epd_type == "epd7in5bc_bw":
        fb.rect(10, 10, EPD_WIDTH - 20, EPD_HEIGHT - 20, 0)
        fb.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf, fb_red.buf)
    else:
        fb.rect(10, 10, EPD_WIDTH - 20, EPD_HEIGHT - 20, 0)
        fb.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf)

except KeyboardInterrupt:    
    print("ctrl + c:")
    exit()