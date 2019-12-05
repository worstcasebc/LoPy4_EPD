import time
import config
from machine import Pin, SPI
import uos

spi = SPI(0, mode=SPI.MASTER, baudrate=2000000, polarity=0, phase=0)

# Display resolution
EPD_WIDTH       = 400
EPD_HEIGHT      = 300

class EPD:
    def __init__(self):
        self.reset_pin = Pin(config.RST_PIN, mode=Pin.OUT)
        self.dc_pin = Pin(config.DC_PIN, mode=Pin.OUT)
        self.busy_pin = Pin(config.BUSY_PIN, mode=Pin.IN)
        self.cs_pin = cs  = Pin(config.CS_PIN, mode=Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

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
        while(self.busy_pin == 0):
            time.sleep_ms(100)
            
    def init(self):
        self.reset()

        self.send_command(0x06) # BOOSTER_SOFT_START
        self.send_data (0x17)
        self.send_data (0x17)
        self.send_data (0x17) # 07 0f 17 1f 27 2F 37 2f
        
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()
        
        self.send_command(0x00) # PANEL_SETTING
        self.send_data(0x0F) # LUT from OTP
        
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

    def display(self, imageblack, imagered):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])
        
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])
        
        self.send_command(0x12) 
        self.ReadBusy()
        
    def Clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
            
        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        
        self.send_command(0x12) 
        self.ReadBusy()

    def sleep(self):
        self.send_command(0x02) # POWER_OFF
        self.ReadBusy()
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0xA5) # check code
        
### END OF FILE ###
