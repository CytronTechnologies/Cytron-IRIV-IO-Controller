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


# Supply voltage (mV).
SUPPLY_VOLTAGE = 3320



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



# Initialize analog inputs.
an0 = analogio.AnalogIn(board.AN0)
an1 = analogio.AnalogIn(board.AN1)



# Read analog voltage (mV).
def an_read_voltage_mv(channel: int):
    adc_val = 0
    if (channel == 0): adc_val = an0.value
    if (channel == 1): adc_val = an1.value
    
    result = adc_val * (SUPPLY_VOLTAGE / 65535 * 16 / 5)
    return int(result)



# Read analog current (uA).
def an_read_current_ua(channel: int):
    adc_val = 0
    if (channel == 0): adc_val = an0.value
    if (channel == 1): adc_val = an1.value
    
    result = adc_val * (SUPPLY_VOLTAGE / 65535 * 16 / 5 / 248 * 1000)
    return int(result)
