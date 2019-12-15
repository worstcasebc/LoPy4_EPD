import time
import pycom
import config
from machine import SPI
import textwrap
import disp_framebuf

#epd_type = "epd2in7"
#epd_type = "epd4in2"
epd_type = "epd4in2bc"
#epd_type = "epd7in5bc"

font_name = "fonts/palatino14"
font = __import__(font_name)

rotation = 1

if epd_type == "epd2in7":
    # Setting for 2in7 display
    from worstcase_epd import epd2in7
    epd = epd2in7.EPD()
    buf = bytearray((epd.width // 8) * epd.height)
    for i in range (len(buf)):
        buf[i] = 0xFF
    fb = disp_framebuf.FrameBuffer(buf, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fb.rotation = rotation
    
elif epd_type == "epd4in2":
    # Setting for 4in2 display
    from worstcase_epd import epd4in2
    epd = epd4in2.EPD()
    buf = bytearray((epd.width // 8) * epd.height)
    for i in range (len(buf)):
        buf[i] = 0xFF
    fb = disp_framebuf.FrameBuffer(buf, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fb.rotation = rotation
    
elif (epd_type == "epd4in2bc"):
    # Setting for 4in2 display
    from worstcase_epd import epd4in2bc
    epd = epd4in2bc.EPD()
    buf = bytearray((epd.width // 8) * epd.height)
    bufc = bytearray((epd.width // 8) * epd.height)
    for i in range (len(buf)):
        buf[i] = 0xFF
        bufc[i] = 0xFF
    fb = disp_framebuf.FrameBuffer(buf, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fbc = disp_framebuf.FrameBuffer(bufc, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fb.rotation = rotation
    fbc.rotation = rotation

elif (epd_type == "epd7in5bc"):
    # Setting for 7in5 display
    from worstcase_epd import epd7in5bc
    epd = epd7in5bc.EPD()
    buf = bytearray((epd.width // 8) * epd.height)
    bufc = bytearray((epd.width // 8) * epd.height)
    for i in range (len(buf)):
        buf[i] = 0xFF
        bufc[i] = 0xFF
    fb = disp_framebuf.FrameBuffer(buf, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fbc = disp_framebuf.FrameBuffer(bufc, epd.width, epd.height, buf_format=disp_framebuf.MHMSB)
    fb.rotation = rotation
    fbc.rotation = rotation
    
else:
    print("Please set a display-type")

# font size
fWidth = font.max_width() 
fHeight = font.height()
tRow = 0

try:
    epd.init()
    
    if rotation in (1, 3):
        screenWidth = epd.height
        screenHeight = epd.width
    else:
        screenWidth = epd.width
        screenHeight = epd.height
    
    # open file and read the text
    print("read text")
    textFile = open('sample_text.txt','r')
    data=textFile.read()
    textFile.close()

    tMaxRow = (screenHeight - (2 * fHeight)) // fHeight

    widthArray = font.getWidthArray()
    print("wrap text")
    sElem = textwrap.wrapWidth(data, screenWidth - (2 * fWidth), widthArray, tMaxRow, linebreak=True)

    tRow = tMaxRow if (len(sElem) > tMaxRow) else len(sElem)

    print("fill framebuffer")
    for i in range(tRow):
        fb.printLine(sElem[i], fWidth + 1, ((i + 1) * fHeight), font_name, color=0x00, size=1)

    if(epd_type == "epd7in5bc") or (epd_type == "epd4in2bc"):
        fbc.line(10,10,screenWidth-10,screenHeight-10,0x00)
        fbc.line(10,screenHeight-10,screenWidth-10,10,0x00)
    else:
        fb.line(10,10,screenWidth-10,screenHeight-10,0x00)
        fb.line(10,screenHeight-10,screenWidth-10,10,0x00)
    
    print("display framebuffer")
    if(epd_type == "epd7in5bc") or (epd_type == "epd4in2bc"):
        epd.display(fb.buf, fbc.buf)
        time.sleep_ms(10000)
    else:
        epd.display(fb.buf)
        time.sleep_ms(5000)
    
    epd.sleep()

except Exception as e:    
    print("Error: {}".format(e))