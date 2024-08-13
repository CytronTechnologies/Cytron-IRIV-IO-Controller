# SPDX-FileCopyrightText: 2024 Wai Weng for Cytron Technologies
#
# SPDX-License-Identifier: MIT

"""
DESCRIPTION:
Registers definiton for MODBUS

AUTHOR  : Wai Weng
COMPANY : Cytron Technologies Sdn Bhd
WEBSITE : www.cytron.io
EMAIL   : support@cytron.io
"""

import os
import board
import iriv_ioc_hal as Hal
from umodbus.serial import ModbusRTU



# Register address.
# Coils (0x)
DO0_ADD = 0x0100
DO1_ADD = 0x0101
DO2_ADD = 0x0102
DO3_ADD = 0x0103

# Contacts (1x)
DI0_ADD = 0x0000
DI1_ADD = 0x0001
DI2_ADD = 0x0002
DI3_ADD = 0x0003
DI4_ADD = 0x0004
DI5_ADD = 0x0005
DI6_ADD = 0x0006
DI7_ADD = 0x0007
DI8_ADD = 0x0008
DI9_ADD = 0x0009
DI10_ADD = 0x000a

# Input Registers (3x)
ANV0_ADD = 0x0200
ANV1_ADD = 0x0201

ANA0_ADD = 0x0210
ANA1_ADD = 0x0211



# MODBUS RTU Client/Slave setup
client = ModbusRTU(
    addr = os.getenv("MODBUS_RTU_SLAVE_ADDRESS"),
    tx_pin = board.TX,
    rx_pin = board.RX,
    baudrate = os.getenv("MODBUS_RTU_BAUDRATE")
)



# Call back for digital outputs.
def dout_set_cb(reg_type, address, val):
    Hal.dout0.value = client.get_coil(DO0_ADD)
    Hal.dout1.value = client.get_coil(DO1_ADD)
    Hal.dout2.value = client.get_coil(DO2_ADD)
    Hal.dout3.value = client.get_coil(DO3_ADD)

# Call back for digital inputs.
def din_get_cb(reg_type, address, val):
    client.set_ist(DI0_ADD, Hal.din0.value)
    client.set_ist(DI1_ADD, Hal.din1.value)
    client.set_ist(DI2_ADD, Hal.din2.value)
    client.set_ist(DI3_ADD, Hal.din3.value)
    client.set_ist(DI4_ADD, Hal.din4.value)
    client.set_ist(DI5_ADD, Hal.din5.value)
    client.set_ist(DI6_ADD, Hal.din6.value)
    client.set_ist(DI7_ADD, Hal.din7.value)
    client.set_ist(DI8_ADD, Hal.din8.value)
    client.set_ist(DI9_ADD, Hal.din9.value)
    client.set_ist(DI10_ADD, Hal.din10.value)

# Call back for analog inputs.
def an_get_cb(reg_type, address, val):
    if (address == ANV0_ADD or address == ANV1_ADD):
        client.set_ireg(ANV0_ADD, Hal.an_read_voltage_mv(0))
        client.set_ireg(ANV1_ADD, Hal.an_read_voltage_mv(1))
        
    elif (address == ANA0_ADD or address == ANA1_ADD):
        client.set_ireg(ANA0_ADD, Hal.an_read_current_ua(0))
        client.set_ireg(ANA1_ADD, Hal.an_read_current_ua(1))



# MODBUS register definitons.
register_definitions = {
    # Coils (0x) - Single bit output (Read/Write).
    "COILS": {
        "DO0": { "register": DO0_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO1": { "register": DO1_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO2": { "register": DO2_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO3": { "register": DO3_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb }
    },
    
    
    # Contacts / Discrete Input (1x) - Single bit input (Read only).
    "ISTS": {
        "DI0": { "register": DI0_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI1": { "register": DI1_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI2": { "register": DI2_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI3": { "register": DI3_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI4": { "register": DI4_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI5": { "register": DI5_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI6": { "register": DI6_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI7": { "register": DI7_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI8": { "register": DI8_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI9": { "register": DI9_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI10": { "register": DI10_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb }
    },
    
    
    # Input Registers (3x) - 16-bit input (Read only).
    "IREGS": {
        "ANV0": { "register": ANV0_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANV1": { "register": ANV1_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANA0": { "register": ANA0_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANA1": { "register": ANA1_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb }
    },
    
    
    # Holding Registers (4x) - 16-bit data (Read/Write).
    "HREGS": {
        "EXAMPLE_HREG": { "register": 93, "len": 1, "val": 19 }
    }
}



# use the defined values of each register type provided by register_definitions
client.setup_registers(registers = register_definitions)
