# always be sure not to push real credentials to GIT
# git update-index --assume-unchanged config.py
WiFiSSID = "<yourSSIDhere>"
WiFiKey  = "<yourKEYhere>"

# which e-paper display to use
#epd_type = "epd2in7"
epd_type = "epd4in2"
#epd_type = "epd7in5bc_bw"       # use only black&white layer
#epd_type = "epd7in5bc_color"    # also use yellow/red layer

epd_rotation = 1

# Mapping e-Paper HAT to LoPy4 as Pxx (and Expansion board Gxx)
RST_PIN  = 'P19'    #G6
DC_PIN   = 'P20'    #G7
BUSY_PIN = 'P18'    #G30
CS_PIN   = 'P4'     #G11
MOSI     = 'P11'    #G22
CLK      = 'P10'    #G17
