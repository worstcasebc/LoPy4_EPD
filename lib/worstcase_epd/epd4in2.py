
import time
import config
from machine import Pin, SPI
import uos
import disp_framebuf

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
        self.width = 400
        self.height = 300
        self.GRAY1  = GRAY1 #white
        self.GRAY2  = GRAY2
        self.GRAY3  = GRAY3 #gray
        self.GRAY4  = GRAY4 #Blackest

    lut_vcom0 = [
    0x00, 0x17, 0x00, 0x00, 0x00, 0x02,        
    0x00, 0x17, 0x17, 0x00, 0x00, 0x02,        
    0x00, 0x0A, 0x01, 0x00, 0x00, 0x01,        
    0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_ww = [
    0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bw = [
    0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_wb = [
    0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bb = [
    0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #******************************gray*********************************/
    #0~3 gray
    EPD_4IN2_4Gray_lut_vcom =[
    0x00	,0x0A	,0x00	,0x00	,0x00	,0x01,
    0x60	,0x14	,0x14	,0x00	,0x00	,0x01,
    0x00	,0x14	,0x00	,0x00	,0x00	,0x01,
    0x00	,0x13	,0x0A	,0x01	,0x00	,0x01,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00
    ]
    #R21
    EPD_4IN2_4Gray_lut_ww =[
    0x40	,0x0A	,0x00	,0x00	,0x00	,0x01,
    0x90	,0x14	,0x14	,0x00	,0x00	,0x01,
    0x10	,0x14	,0x0A	,0x00	,0x00	,0x01,
    0xA0	,0x13	,0x01	,0x00	,0x00	,0x01,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    ]
    #R22H	r
    EPD_4IN2_4Gray_lut_bw =[
    0x40	,0x0A	,0x00	,0x00	,0x00	,0x01,
    0x90	,0x14	,0x14	,0x00	,0x00	,0x01,
    0x00	,0x14	,0x0A	,0x00	,0x00	,0x01,
    0x99	,0x0C	,0x01	,0x03	,0x04	,0x01,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    ]
    #R23H	w
    EPD_4IN2_4Gray_lut_wb =[
    0x40	,0x0A	,0x00	,0x00	,0x00	,0x01,
    0x90	,0x14	,0x14	,0x00	,0x00	,0x01,
    0x00	,0x14	,0x0A	,0x00	,0x00	,0x01,
    0x99	,0x0B	,0x04	,0x04	,0x01	,0x01,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    ]
    #R24H	b
    EPD_4IN2_4Gray_lut_bb =[
    0x80	,0x0A	,0x00	,0x00	,0x00	,0x01,
    0x90	,0x14	,0x14	,0x00	,0x00	,0x01,
    0x20	,0x14	,0x0A	,0x00	,0x00	,0x01,
    0x50	,0x13	,0x01	,0x00	,0x00	,0x01,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
    0x00	,0x00	,0x00	,0x00	,0x00	,0x00,
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
        self.send_command(0x71)
        while(self.busy_pin == 0):      #  0: idle, 1: busy
            self.send_command(0x71)
            time.sleep_ms(200)   

    def set_lut(self):
        self.send_command(0x20)               # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom0[count])
            
        self.send_command(0x21)         # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
            
        self.send_command(0x22)         # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
            
        self.send_command(0x23)         # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
            
        self.send_command(0x24)         # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
        
    def Gray_SetLut(self):
        self.send_command(0x20)						#vcom
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_vcom[count]) 

        self.send_command(0x21)						#red not use
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_ww[count]) 

        self.send_command(0x22)							#bw r
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_bw[count]) 

        self.send_command(0x23)							#wb w
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_wb[count]) 

        self.send_command(0x24)                          #bb b
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_bb[count]) 

        self.send_command(0x25)						#vcom
        for count in range(0, 42):
            self.send_data(self.EPD_4IN2_4Gray_lut_ww[count])
      
    
    def init(self):
        # EPD hardware init start
        self.reset()
        
        self.send_command(0x01) # POWER SETTING
        self.send_data(0x03) # VDS_EN, VDG_EN
        self.send_data(0x00) # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b) # VDH
        self.send_data(0x2b) # VDL
        
        self.send_command(0x06) # boost soft start
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)
        
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()
        
        self.send_command(0x00) # panel setting
        self.send_data(0xbf) # KW-BF   KWR-AF  BWROTP 0f
        self.send_data(0x0d)
        
        self.send_command(0x30) # PLL setting
        self.send_data(0x3c) # 3A 100HZ   29 150Hz 39 200HZ  31 171HZ

        self.send_command(0x61)	# resolution setting
        self.send_data(0x01)
        self.send_data(0x90) # 128
        self.send_data(0x01)		
        self.send_data(0x2c)

        self.send_command(0x82)	# vcom_DC setting
        self.send_data(0x28)

        self.send_command(0X50)	# VCOM AND DATA INTERVAL SETTING
        self.send_data(0x97) # 97white border 77black border		VBDF 17|D7 VBDW 97 VBDB 57		VBDF F7 VBDW 77 VBDB 37  VBDR B7
    
        self.set_lut()
        # EPD hardware init end
        return 0
        
    def Init_4Gray(self):
        # EPD hardware init start
        self.reset()
        
        self.send_command(0x01)			#POWER SETTING
        self.send_data (0x03)
        self.send_data (0x00)       #VGH=20V,VGL=-20V
        self.send_data (0x2b)		#VDH=15V															 
        self.send_data (0x2b)		#VDL=-15V
        self.send_data (0x13)

        self.send_command(0x06)         #booster soft start
        self.send_data (0x17)		#A
        self.send_data (0x17)		#B
        self.send_data (0x17)		#C 

        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0x00)			#panel setting
        self.send_data(0x3f)		#KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x30)			#PLL setting
        self.send_data (0x3c)      	#100hz 

        self.send_command(0x61)			#resolution setting
        self.send_data (0x01)		#400
        self.send_data (0x90)     	 
        self.send_data (0x01)		#300
        self.send_data (0x2c)

        self.send_command(0x82)			#vcom_DC setting
        self.send_data (0x12)

        self.send_command(0X50)			#VCOM AND DATA INTERVAL SETTING			
        self.send_data(0x97)

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
        
    def getbuffer_4Gray(self, image):
        buf = [0xFF] * (int(self.width / 4) * self.height)
        image_monocolor = image.convert('L')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        i=0
        if(imwidth == self.width and imheight == self.height):
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((x + (y * self.width))/4)] = ((pixels[x-3, y]&0xc0) | (pixels[x-2, y]&0xc0)>>2 | (pixels[x-1, y]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6)
                        
        elif(imwidth == self.height and imheight == self.width):
            for x in range(imwidth):
                for y in range(imheight):
                    newx = y
                    newy = x
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((newx + (newy * self.width))/4)] = ((pixels[x, y-3]&0xc0) | (pixels[x, y-2]&0xc0)>>2 | (pixels[x, y-1]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6) 
        
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
    
    def display_4Gray(self, image):
        self.send_command(0x10)
        for i in range(0, EPD_WIDTH * EPD_HEIGHT / 8):                   # EPD_WIDTH * EPD_HEIGHT / 4
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80): 
                        temp3 |= 0x01  #gray1
                    else: #0x40
                        temp3 |= 0x00 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x01 #gray1
                    else :   #0x40
                            temp3 |= 0x00	#gray2	
                    if(j!=1 or k!=1):				
                        temp3 <<= 1
                    temp1 <<= 2
            self.send_data(temp3)
            
        self.send_command(0x13)	    
               
        for i in range(0, EPD_WIDTH * EPD_HEIGHT / 8):                #5808*4  46464
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80):
                        temp3 |= 0x00  #gray1
                    else: #0x40
                        temp3 |= 0x01 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x00 #gray1
                    else:    #0x40
                            temp3 |= 0x01	#gray2
                    if(j!=1 or k!=1):					
                        temp3 <<= 1
                    temp1 <<= 2
            self.send_data(temp3)
        
        self.Gray_SetLut()
        self.send_command(0x12)
        epdconfig.delay_ms(200)
        self.ReadBusy()
        # pass
    
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
        self.send_data(0XA5)
        
### END OF FILE ###
