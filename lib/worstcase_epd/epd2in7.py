import time
import config
from machine import Pin, SPI
import uos

spi = SPI(0, mode=SPI.MASTER, baudrate=2000000, polarity=0, phase=0)

GRAY1  = 0xff #white
GRAY2  = 0xC0
GRAY3  = 0x80 #gray
GRAY4  = 0x00 #Blackest

class EPD():
    def __init__(self):
        self.reset_pin = Pin(config.RST_PIN, mode=Pin.OUT)
        self.dc_pin = Pin(config.DC_PIN, mode=Pin.OUT)
        self.busy_pin = Pin(config.BUSY_PIN, mode=Pin.IN)
        self.cs_pin = cs  = Pin(config.CS_PIN, mode=Pin.OUT)
        self.width = 176
        self.height = 264
        self.GRAY1  = GRAY1 #white
        self.GRAY2  = GRAY2
        self.GRAY3  = GRAY3 #gray
        self.GRAY4  = GRAY4 #Blackest

    lut_vcom_dc = [0x00, 0x00,
        0x00, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x60, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    lut_ww = [
        0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
        0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bw = [
        0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
        0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bb = [
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_wb = [
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    ###################full screen update LUT######################
    #0~3 gray
    gray_lut_vcom = [
    0x00, 0x00,
    0x00, 0x0A, 0x00, 0x00, 0x00, 0x01,
    0x60, 0x14, 0x14, 0x00, 0x00, 0x01,
    0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x13, 0x0A, 0x01, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,				
    ]
    #R21
    gray_lut_ww =[
    0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
    0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
    0x10, 0x14, 0x0A, 0x00, 0x00, 0x01,
    0xA0, 0x13, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    #R22H	r
    gray_lut_bw =[
    0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
    0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
    0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
    0x99, 0x0C, 0x01, 0x03, 0x04, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    #R23H	w
    gray_lut_wb =[
    0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
    0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
    0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
    0x99, 0x0B, 0x04, 0x04, 0x01, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    #R24H	b
    gray_lut_bb =[
    0x80, 0x0A, 0x00, 0x00, 0x00, 0x01,
    0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
    0x20, 0x14, 0x0A, 0x00, 0x00, 0x01,
    0x50, 0x13, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    # Hardware reset
    def reset(self):
        self.reset_pin(1)
        time.sleep_ms(200) 
        self.reset_pin(0)
        time.sleep_ms(10)
        self.reset_pin(1)
        time.sleep_ms(200)   

    def send_command(self, command):
        self.dc_pin(0)
        self.cs_pin(0)
        spi.write(command)
        self.cs_pin(1)

    def send_data(self, data):
        self.dc_pin(1)
        self.cs_pin(0)
        spi.write(data)
        self.cs_pin(1)
        
    def ReadBusy(self):        
        while(self.busy_pin == 0):      #  0: idle, 1: busy
            time.sleep_ms(200)                

    def set_lut(self):
        self.send_command(0x20) # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom_dc[count])
        self.send_command(0x21) # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
        self.send_command(0x22) # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
        self.send_command(0x23) # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
        self.send_command(0x24) # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
            
    def gray_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):        #vcom
            self.send_data(self.gray_lut_vcom[count])
            
        self.send_command(0x21)							#red not use
        for count in range(0, 42): 
            self.send_data(self.gray_lut_ww[count])

        self.send_command(0x22)							#bw r
        for count in range(0, 42): 
            self.send_data(self.gray_lut_bw[count])

        self.send_command(0x23)							#wb w
        for count in range(0, 42): 
            self.send_data(self.gray_lut_wb[count])

        self.send_command(0x24)							#bb b
        for count in range(0, 42): 
            self.send_data(self.gray_lut_bb[count])

        self.send_command(0x25)							#vcom
        for count in range(0, 42): 
            self.send_data(self.gray_lut_ww[count])
    
    def init(self):
        # EPD hardware init start
        self.reset()
        
        self.send_command(0x01) # POWER_SETTING
        self.send_data(0x03) # VDS_EN, VDG_EN
        self.send_data(0x00) # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b) # VDH
        self.send_data(0x2b) # VDL
        self.send_data(0x09) # VDHR
        
        self.send_command(0x06) # BOOSTER_SOFT_START
        self.send_data(0x07)
        self.send_data(0x07)
        self.send_data(0x17)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x60)
        self.send_data(0xA5)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x89)
        self.send_data(0xA5)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x90)
        self.send_data(0x00)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x93)
        self.send_data(0x2A)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0xA0)
        self.send_data(0xA5)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0xA1)
        self.send_data(0x00)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x73)
        self.send_data(0x41)
        
        self.send_command(0x16) # PARTIAL_DISPLAY_REFRESH
        self.send_data(0x00)
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()

        self.send_command(0x00) # PANEL_SETTING
        self.send_data(0xAF) # KW-BF   KWR-AF    BWROTP 0f
        
        self.send_command(0x30) # PLL_CONTROL
        self.send_data(0x3A) # 3A 100HZ   29 150Hz 39 200HZ    31 171HZ
        
        self.send_command(0x82) # VCM_DC_SETTING_REGISTER
        self.send_data(0x12)
        self.set_lut()
        return 0

    def getbuffer(self, image):
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if(imwidth == self.width and imheight == self.height):
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf
    
    def display(self, buf):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(buf[i])
        self.send_command(0x12) 
        self.ReadBusy()

    def Clear(self, color=GRAY1):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(color)
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(color)
        self.send_command(0x12) 
        self.ReadBusy()

    def sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)
        self.send_command(0X07)
        self.send_data(0xA5)
### END OF FILE ###