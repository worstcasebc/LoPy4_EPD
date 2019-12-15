import time
import config
from machine import Pin, SPI
import uos

spi = SPI(0, mode=SPI.MASTER, baudrate=2000000, polarity=0, phase=0)

class EPD():
    def __init__(self):
        self.reset_pin = Pin(config.RST_PIN, mode=Pin.OUT)
        self.dc_pin = Pin(config.DC_PIN, mode=Pin.OUT)
        self.busy_pin = Pin(config.BUSY_PIN, mode=Pin.IN)
        self.cs_pin = cs  = Pin(config.CS_PIN, mode=Pin.OUT)
        self.width = 640
        self.height = 384

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
         while(self.busy_pin == 1):      # 0: idle, 1: busy
            time.sleep_ms(100)
            
    def init(self):
          
        self.reset()

        self.send_command(0x01) # POWER_SETTING
        self.send_data(0x37)
        self.send_data(0x00)
        
        self.send_command(0x00) # PANEL_SETTING
        self.send_data(0xCF)
        self.send_data(0x08)
        
        self.send_command(0x30) # PLL_CONTROL
        self.send_data(0x3A) # PLL:  0-15:0x3C, 15+:0x3A
        
        self.send_command(0x82) # VCM_DC_SETTING
        self.send_data(0x28) #all temperature  range

        self.send_command(0x06) # BOOSTER_SOFT_START
        self.send_data(0xc7)
        self.send_data(0xcc)
        self.send_data(0x15)

        self.send_command(0x50) # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x76)

        self.send_command(0x60) # TCON_SETTING
        self.send_data(0x22) # 11 is possible too

        self.send_command(0x65) # FLASH CONTROL
        self.send_data(0x00)

        self.send_command(0x61) # TCON_RESOLUTION
        self.send_data(self.width >> 8) # source 640
        self.send_data(self.width & 0xff)
        self.send_data(self.height >> 8) # gate 384
        self.send_data(self.height & 0xff)

        self.send_command(0xe5) # FLASH MODE
        self.send_data(0x03)
        
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

    def display(self, buf, bufc):
        self.send_command(0x10)
        for i in range(0, int(self.width / 8 * self.height)):
            temp1 = buf[i]
            temp2 = bufc[i]
            j = 0
            while (j < 8):
                if ((temp2 & 0x80) == 0x00):
                    temp3 = 0x04                #red
                elif ((temp1 & 0x80) == 0x00):
                    temp3 = 0x00                #black
                else:
                    temp3 = 0x03                #white
					
                temp3 = (temp3 << 4) & 0xFF
                temp1 = (temp1 << 1) & 0xFF
                temp2 = (temp2 << 1) & 0xFF
                j += 1
                if((temp2 & 0x80) == 0x00):
                    temp3 |= 0x04              #red
                elif ((temp1 & 0x80) == 0x00):
                    temp3 |= 0x00              #black
                else:
                    temp3 |= 0x03              #white
                temp1 = (temp1 << 1) & 0xFF
                temp2 = (temp2 << 1) & 0xFF
                self.send_data(temp3)
                j += 1
        self.send_command(0x04) # POWER ON
        self.ReadBusy()
        self.send_command(0x12) # display refresh
        self.ReadBusy()
        
    def Clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width / 8 * self.height)):
            self.send_data(0x44)
            self.send_data(0x44)
            self.send_data(0x44)
            self.send_data(0x44)
            
        self.send_command(0x04) # POWER ON
        self.ReadBusy()
        self.send_command(0x12) # display refresh
        self.ReadBusy()

    def sleep(self):
        self.send_command(0x02) # POWER_OFF
        self.ReadBusy()
        
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)

### END OF FILE ###

