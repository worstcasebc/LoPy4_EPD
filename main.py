import time
import pycom
import config
import adafruit_framebuf
from machine import SPI
import textwrap

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
elif config.epd_type == "epd4in2bc":
    # Setting for 4in2 display
    from waveshare_epd import epd4in2bc
    EPD_WIDTH       = 400
    EPD_HEIGHT      = 300
    epd = epd4in2bc.EPD()
elif (config.epd_type == "epd7in5bc_color") or (config.epd_type == "epd7in5bc_bw"):
    # Setting for 7in5 display
    from waveshare_epd import epd7in5bc
    EPD_WIDTH       = 640
    EPD_HEIGHT      = 384
    epd = epd7in5bc.EPD()
else:
    print("Please set a display-type within config.py")

# font size
fWidth = 6
fHeight = 8

try:
    epd.init()

    bab = bytearray(EPD_WIDTH * EPD_HEIGHT // 8)
    for i in range(len(bab)):
        bab[i] = 0xFF
    fb = adafruit_framebuf.FrameBuffer(bab, EPD_WIDTH, EPD_HEIGHT, buf_format=adafruit_framebuf.MHMSB)
    fb.rotation = config.epd_rotation

    if (config.epd_type == "epd7in5bc_color") or (config.epd_type == "epd7in5bc_bw") or (config.epd_type == "epd4in2bc"):
        bay = bytearray(EPD_WIDTH * EPD_HEIGHT // 8)
        for i in range(len(bay)):
            bay[i] = 0xFF
        fb_red = adafruit_framebuf.FrameBuffer(bay, EPD_WIDTH, EPD_HEIGHT, buf_format=adafruit_framebuf.MHMSB)
        fb_red.rotation = config.epd_rotation

    if config.epd_rotation in (1, 3):
        tmp_width = EPD_WIDTH
        EPD_WIDTH = EPD_HEIGHT
        EPD_HEIGHT = tmp_width
    
    # max num of lines and columns for the font of 6x8
    tColMax = (EPD_WIDTH - (2 * fWidth)) // fWidth
    tRowMax = (EPD_HEIGHT - (2 * fHeight)) // fHeight

    print("Display-size: {} x {}".format(EPD_WIDTH, EPD_HEIGHT))
    print("Num of Rows {} / Cols {}".format(tRowMax, tColMax))

    # open file and read the text
    textFile = open('sample_text.txt','r')
    data=textFile.read()
    textFile.close()

    sElem = textwrap.wrap(data, tColMax, linebreak=True)
    #print(len(sElem))

    if (len(sElem) > tRowMax):
        tRow = tRowMax
    else:
        tRow = len(sElem)

    for i in range(tRow):
        # the adafruit-frambuffer is not working for special chars (e.g. " ' ")
        #print("[{}]: {}".format(i, sElem[i]))
        fb_red.text(sElem[i], fWidth, (i+1) * fHeight + 1, 0)
        
    if config.epd_type == "epd7in5bc_color":
        fb_red.rect(2, 2, EPD_WIDTH - 4, EPD_HEIGHT - 4, 0)
        #fb_red.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf, fb_red.buf)
    elif config.epd_type == "epd7in5bc_bw":
        fb.rect(2, 2, EPD_WIDTH - 4, EPD_HEIGHT - 4, 0)
        #fb.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf, fb_red.buf)
    elif config.epd_type == "epd4in2bc":
        fb.rect(2, 2, EPD_WIDTH - 4, EPD_HEIGHT - 4, 0)
        #fb.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf, fb_red.buf)
    else:
        fb.rect(2, 2, EPD_WIDTH - 4, EPD_HEIGHT - 4, 0)
        #fb.fill_rect(EPD_WIDTH // 2, EPD_HEIGHT // 2, 60, 60, 0)
        epd.display(fb.buf)

    time.sleep_ms(20000)
    epd.sleep()

except KeyboardInterrupt:    
    print("ctrl + c:")
    exit()