# SPDX-FileCopyrightText: 2024 Wai Weng for Cytron Technologies
#
# SPDX-License-Identifier: MIT

"""
DESCRIPTION:
Hardware Abstraction Layer (HAL) for IRIV-IOC.
Include libraries and functions for the hardware.

AUTHOR  : Wai Weng
COMPANY : Cytron Technologies Sdn Bhd
WEBSITE : www.cytron.io
EMAIL   : support@cytron.io
"""

import board
import digitalio
import analogio
import busio
import countio


# Supply voltage (mV).
SUPPLY_VOLTAGE = 3320



# Initialize LED.
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = 0



# Initialize digital outputs.
dout0 = digitalio.DigitalInOut(board.DO0)
dout1 = digitalio.DigitalInOut(board.DO1)
dout2 = digitalio.DigitalInOut(board.DO2)
dout3 = digitalio.DigitalInOut(board.DO3)

dout0.direction = digitalio.Direction.OUTPUT
dout1.direction = digitalio.Direction.OUTPUT
dout2.direction = digitalio.Direction.OUTPUT
dout3.direction = digitalio.Direction.OUTPUT

dout0.value = 0
dout1.value = 0
dout2.value = 0
dout3.value = 0



# Initialize digital inputs.
din0 = digitalio.DigitalInOut(board.DI0)
din1 = digitalio.DigitalInOut(board.DI1)
din2 = digitalio.DigitalInOut(board.DI2)
din3 = digitalio.DigitalInOut(board.DI3)
din4 = digitalio.DigitalInOut(board.DI4)
din5 = digitalio.DigitalInOut(board.DI5)
din6 = digitalio.DigitalInOut(board.DI6)
din7 = digitalio.DigitalInOut(board.DI7)
din8 = digitalio.DigitalInOut(board.DI8)
din9 = digitalio.DigitalInOut(board.DI9)
din10 = digitalio.DigitalInOut(board.DI10)

din0.direction = digitalio.Direction.INPUT
din1.direction = digitalio.Direction.INPUT
din2.direction = digitalio.Direction.INPUT
din3.direction = digitalio.Direction.INPUT
din4.direction = digitalio.Direction.INPUT
din5.direction = digitalio.Direction.INPUT
din6.direction = digitalio.Direction.INPUT
din7.direction = digitalio.Direction.INPUT
din8.direction = digitalio.Direction.INPUT
din9.direction = digitalio.Direction.INPUT
din10.direction = digitalio.Direction.INPUT



# SPI for W5500.
w5500_cs = digitalio.DigitalInOut(board.W5500_CS)
w5500_rst = digitalio.DigitalInOut(board.W5500_RST)
w5500_spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)



# Counter objects.
count1 = None
count3 = None
count5 = None
count7 = None
count9 = None



# Initialize analog inputs.
an0 = analogio.AnalogIn(board.AN0)
an1 = analogio.AnalogIn(board.AN1)



# Read analog voltage (mV).
def an_read_voltage_mv(channel: int) -> int:
    adc_val = 0
    if (channel == 0): adc_val = an0.value
    if (channel == 1): adc_val = an1.value
    
    result = adc_val * (SUPPLY_VOLTAGE / 65535 * 16 / 5)
    return int(result)



# Read analog current (uA).
def an_read_current_ua(channel: int) -> int:
    adc_val = 0
    if (channel == 0): adc_val = an0.value
    if (channel == 1): adc_val = an1.value
    
    result = adc_val * (SUPPLY_VOLTAGE / 65535 * 16 / 5 / 248 * 1000)
    return int(result)



# Enable counter.
# Return False if counter is already enabled before.
def en_counter(channel: int):
    global count1
    global count3
    global count5
    global count7
    global count9
    
    if (channel == 1 and count1 == None):
        din1.deinit()
        count1 = countio.Counter(board.DI1, edge=countio.Edge.FALL)
        return True
        
    if (channel == 3 and count3 == None):
        din3.deinit()
        count3 = countio.Counter(board.DI3, edge=countio.Edge.FALL)
        return True
        
    if (channel == 5 and count5 == None):
        din5.deinit()
        count5 = countio.Counter(board.DI5, edge=countio.Edge.FALL)
        return True
        
    if (channel == 7 and count7 == None):
        din7.deinit()
        count7 = countio.Counter(board.DI7, edge=countio.Edge.FALL)
        return True
        
    if (channel == 9 and count9 == None):
        din9.deinit()
        count9 = countio.Counter(board.DI9, edge=countio.Edge.FALL)
        return True
    
    return False



# Disable counter.
# Return False if counter is already disabled before.
def dis_counter(channel: int):
    global count1
    global count3
    global count5
    global count7
    global count9
    
    global din1
    global din3
    global din5
    global din7
    global din9
    
    # we need to check whether the counter is enabled before.
    # Then only continue to deinitialize the counter and initialize the digital input.
    
    if (channel == 1 and count1 != None):
        count1.deinit()
        count1 = None
        din1 = digitalio.DigitalInOut(board.DI1)
        din1.direction = digitalio.Direction.INPUT
        return True
        
    if (channel == 3 and count3 != None):
        count3.deinit()
        count3 = None
        din3 = digitalio.DigitalInOut(board.DI3)
        din3.direction = digitalio.Direction.INPUT
        return True
        
    if (channel == 5 and count5 != None):
        count5.deinit()
        count5 = None
        din5 = digitalio.DigitalInOut(board.DI5)
        din5.direction = digitalio.Direction.INPUT
        return True
        
    if (channel == 7 and count7 != None):
        count7.deinit()
        count7 = None
        din7 = digitalio.DigitalInOut(board.DI7)
        din7.direction = digitalio.Direction.INPUT
        return True
        
    if (channel == 9 and count9 != None):
        count9.deinit()
        count9 = None
        din9 = digitalio.DigitalInOut(board.DI9)
        din9.direction = digitalio.Direction.INPUT
        return True
    
    return False
        