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
import time
import board
import microcontroller
import iriv_ioc_hal as Hal
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socketpool as socketpool
from umodbus.serial import ModbusRTU
from umodbus.tcp import ModbusTCP



# Model Name
MODEL1 = 0x494F  # "IO"
MODEL2 = 0x4300  # "C"

# Version
VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_PATCH = 0



# Register address.
# Coils (0x) - Read/Write
DO0_ADD = 0x0100        # Digital Output 0
DO1_ADD = 0x0101        # Digital Output 1
DO2_ADD = 0x0102        # Digital Output 2
DO3_ADD = 0x0103        # Digital Output 3

COUNT1_EN_ADD = 0x0300  # Counter Enable for Digital Input 1
COUNT3_EN_ADD = 0x0301  # Counter Enable for Digital Input 3
COUNT5_EN_ADD = 0x0302  # Counter Enable for Digital Input 5
COUNT7_EN_ADD = 0x0303  # Counter Enable for Digital Input 7
COUNT9_EN_ADD = 0x0304  # Counter Enable for Digital Input 9

COUNT1_RST_ADD = 0x0310 # Counter Reset for Digital Input 1. Auto clear after read.
COUNT3_RST_ADD = 0x0311 # Counter Reset for Digital Input 1. Auto clear after read.
COUNT5_RST_ADD = 0x0312 # Counter Reset for Digital Input 1. Auto clear after read.
COUNT7_RST_ADD = 0x0313 # Counter Reset for Digital Input 1. Auto clear after read.
COUNT9_RST_ADD = 0x0314 # Counter Reset for Digital Input 1. Auto clear after read.


# Contacts (1x) - Read Only
DI0_ADD = 0x0000        # Digital Input 0
DI1_ADD = 0x0001        # Digital Input 1
DI2_ADD = 0x0002        # Digital Input 2
DI3_ADD = 0x0003        # Digital Input 3
DI4_ADD = 0x0004        # Digital Input 4
DI5_ADD = 0x0005        # Digital Input 5
DI6_ADD = 0x0006        # Digital Input 6
DI7_ADD = 0x0007        # Digital Input 7
DI8_ADD = 0x0008        # Digital Input 8
DI9_ADD = 0x0009        # Digital Input 9
DI10_ADD = 0x000a       # Digital Input 10


# Input Registers (3x) - Read Only
ANV0_ADD = 0x0200       # Analog Input 0 (V)
ANV1_ADD = 0x0201       # Analog Input 1 (V)

ANA0_ADD = 0x0210       # Analog Input 0 (mA)
ANA1_ADD = 0x0211       # Analog Input 1 (mA)

COUNT1_H_ADD = 0x0400   # Counter value for Digital Input 1 (Write 0 to reset)
COUNT1_L_ADD = 0x0401
COUNT3_H_ADD = 0x0402   # Counter value for Digital Input 3 (Write 0 to reset)
COUNT3_L_ADD = 0x0403
COUNT5_H_ADD = 0x0404   # Counter value for Digital Input 5 (Write 0 to reset)
COUNT5_L_ADD = 0x0405
COUNT7_H_ADD = 0x0406   # Counter value for Digital Input 7 (Write 0 to reset)
COUNT7_L_ADD = 0x0407
COUNT9_H_ADD = 0x0408   # Counter value for Digital Input 9 (Write 0 to reset)
COUNT9_L_ADD = 0x0409

MODEL1_ADD = 0x0F00     # Model Name 1 (Read Only)
MODEL2_ADD = 0x0F01     # Model Name 2 (Read Only)

VERSION_MAJOR_ADD = 0x0F10  # Major Version (Read Only)
VERSION_MINOR_ADD = 0x0F11  # Minor Version (Read Only)
VERSION_PATCH_ADD = 0x0F12  # Patch Version (Read Only)



# MODBUS RTU Client/Slave setup
modbus_mode = os.getenv("MODBUS_MODE")
if (modbus_mode == "RTU"):
    client = ModbusRTU(
        addr = os.getenv("MODBUS_RTU_SLAVE_ADDRESS"),
        tx_pin = board.TX,
        rx_pin = board.RX,
        baudrate = os.getenv("MODBUS_RTU_BAUDRATE")
    )

# MODBUS TCP Client/Slave setup
else:
    # Construct the MAC address from dummy OUI (first 3 bytes) and board UID (last 3 bytes).
    mac_address = bytearray([0xDE,0xAD,0xBE]) + microcontroller.cpu.uid[-3:]
    
    # Construct the hostname with last 3 bytes of board UID.
    hostname = "IRIV-IOC_" + microcontroller.cpu.uid[-3:].hex().upper()
    
    # Getting IP address from DHCP?
    is_dhcp = bool(os.getenv("DHCP"))
    
    # Turn on USR LED while waiting for the ethernet link to be established.
    Hal.led.value = 1
    
    # Initialize ethernet interface.
    while True:
        try:
            eth = WIZNET5K(Hal.w5500_spi, Hal.w5500_cs, Hal.w5500_rst, is_dhcp=is_dhcp, mac=mac_address, hostname=hostname)
        except Exception:
            # Cannot connect to network. Try again after 1 second.
            time.sleep(1)
            continue
        break
    
    # Wait until link is up.
    while not eth.link_status:
        continue
    
    # Configure the IP Address, Subnet Mask, Gateway and DNS manually if not using DHCP.
    if not is_dhcp:
        # Get the settings for MODBUS TCP.
        ip_address = eth.unpretty_ip(os.getenv("IP_ADDRESS"))
        subnet_mask = eth.unpretty_ip(os.getenv("SUBNET_MASK"))
        gateway_address = eth.unpretty_ip(os.getenv("GATEWAY_ADDRESS"))
        dns_server = eth.unpretty_ip(os.getenv("DNS_SERVER"))
        
        eth.ifconfig = (ip_address, subnet_mask, gateway_address, dns_server)
    
    # Open sockets for listening.
    sockpool = socketpool.SocketPool(eth)
    server_port = 502
    
    client = ModbusTCP(sockpool, addr_list = [0xff])
    client.bind(local_port=502, max_connections=7)
    
    print("MAC Address:", eth.pretty_mac(eth.mac_address))
    print("IP Address:", eth.pretty_ip(eth.ip_address))
    


# Call back when reading DIN.
def din_get_cb(reg_type, address, val):
    
    # For DIN without counter function, set the register value based on DIN value.
    client.set_ist(DI0_ADD,  Hal.din0.value)
    client.set_ist(DI2_ADD,  Hal.din2.value)
    client.set_ist(DI4_ADD,  Hal.din4.value)
    client.set_ist(DI6_ADD,  Hal.din6.value)
    client.set_ist(DI8_ADD,  Hal.din8.value)
    client.set_ist(DI10_ADD, Hal.din10.value)
    
    # For DIN with counter function:
    # Set the register value based on DIN value if counter is disabled.
    # Clear the register value if counter is enabled.
    if (client.get_coil(COUNT1_EN_ADD) == 0): client.set_ist(DI1_ADD, Hal.din1.value)
    else:                                     client.set_ist(DI1_ADD, 0)
    if (client.get_coil(COUNT3_EN_ADD) == 0): client.set_ist(DI3_ADD, Hal.din3.value)
    else:                                     client.set_ist(DI3_ADD, 0)
    if (client.get_coil(COUNT5_EN_ADD) == 0): client.set_ist(DI5_ADD, Hal.din5.value)
    else:                                     client.set_ist(DI5_ADD, 0)
    if (client.get_coil(COUNT7_EN_ADD) == 0): client.set_ist(DI7_ADD, Hal.din7.value)
    else:                                     client.set_ist(DI7_ADD, 0)
    if (client.get_coil(COUNT9_EN_ADD) == 0): client.set_ist(DI9_ADD, Hal.din9.value)
    else:                                     client.set_ist(DI9_ADD, 0)
    
    
    
# Call back when writting DOUT.
def dout_set_cb(reg_type, address, val):
    # Set the DOUT based on register value.
    Hal.dout0.value = client.get_coil(DO0_ADD)
    Hal.dout1.value = client.get_coil(DO1_ADD)
    Hal.dout2.value = client.get_coil(DO2_ADD)
    Hal.dout3.value = client.get_coil(DO3_ADD)
    
    
    
# Call back when reading AN.
def an_get_cb(reg_type, address, val):
    # Reading voltage
    if (address == ANV0_ADD or address == ANV1_ADD):
        client.set_ireg(ANV0_ADD, Hal.an_read_voltage_mv(0))
        client.set_ireg(ANV1_ADD, Hal.an_read_voltage_mv(1))
        
    # Reading current
    elif (address == ANA0_ADD or address == ANA1_ADD):
        client.set_ireg(ANA0_ADD, Hal.an_read_current_ua(0))
        client.set_ireg(ANA1_ADD, Hal.an_read_current_ua(1))



# Call back when setting the Counter Enable Bit.
def counter_en_set_cb(reg_type, address, val):
    # Enable the counter function if the enable bit is set.
    # Clear the counter value if it's just enabled.
    if (client.get_coil(COUNT1_EN_ADD) == 1):
        if (Hal.en_counter(1) == True):
            client.set_ireg(COUNT1_H_ADD, [0, 0])
    else:
        Hal.dis_counter(1)
        
        
    if (client.get_coil(COUNT3_EN_ADD) == 1):
        if (Hal.en_counter(3) == True):
            client.set_ireg(COUNT3_H_ADD, [0, 0])
    else:
        Hal.dis_counter(3)
        
        
    if (client.get_coil(COUNT5_EN_ADD) == 1):
        if (Hal.en_counter(5) == True):
            client.set_ireg(COUNT5_H_ADD, [0, 0])
    else:
        Hal.dis_counter(5)
        
        
    if (client.get_coil(COUNT7_EN_ADD) == 1):
        if (Hal.en_counter(7) == True):
            client.set_ireg(COUNT7_H_ADD, [0, 0])
    else:
        Hal.dis_counter(7)
        
        
    if (client.get_coil(COUNT9_EN_ADD) == 1):
        if (Hal.en_counter(9) == True):
            client.set_ireg(COUNT9_H_ADD, [0, 0])
    else:
        Hal.dis_counter(9)
            
            
            
# Call back when setting the Counter Reset Bit.
def counter_rst_set_cb(reg_type, address, val):
    # If counter reset bit is set, clear the bit and reset the counter.
    # Also clear the counter value register.
    if (client.get_coil(COUNT1_RST_ADD) == 1):
        client.set_coil(COUNT1_RST_ADD, 0)
        Hal.count1.reset()
        client.set_ireg(COUNT1_H_ADD, [0, 0])
        
    if (client.get_coil(COUNT3_RST_ADD) == 1):
        client.set_coil(COUNT3_RST_ADD, 0)
        Hal.count3.reset()
        client.set_ireg(COUNT3_H_ADD, [0, 0])
        
    if (client.get_coil(COUNT5_RST_ADD) == 1):
        client.set_coil(COUNT5_RST_ADD, 0)
        Hal.count5.reset()
        client.set_ireg(COUNT5_H_ADD, [0, 0])
        
    if (client.get_coil(COUNT7_RST_ADD) == 1):
        client.set_coil(COUNT7_RST_ADD, 0)
        Hal.count7.reset()
        client.set_ireg(COUNT7_H_ADD, [0, 0])
        
    if (client.get_coil(COUNT9_RST_ADD) == 1):
        client.set_coil(COUNT9_RST_ADD, 0)
        Hal.count9.reset()
        client.set_ireg(COUNT9_H_ADD, [0, 0])



# Call back when reading the counter value.
def counter_get_cb(reg_type, address, val):
    if (client.get_coil(COUNT1_EN_ADD) == 1):
        count = Hal.count1.count
        client.set_ireg(COUNT1_H_ADD, [count >> 8, count & 0xffff])
        
    if (client.get_coil(COUNT3_EN_ADD) == 1):
        count = Hal.count3.count
        client.set_ireg(COUNT3_H_ADD, [count >> 8, count & 0xffff])
        
    if (client.get_coil(COUNT5_EN_ADD) == 1):
        count = Hal.count5.count
        client.set_ireg(COUNT5_H_ADD, [count >> 8, count & 0xffff])
        
    if (client.get_coil(COUNT7_EN_ADD) == 1):
        count = Hal.count7.count
        client.set_ireg(COUNT7_H_ADD, [count >> 8, count & 0xffff])
        
    if (client.get_coil(COUNT9_EN_ADD) == 1):
        count = Hal.count9.count
        client.set_ireg(COUNT9_H_ADD, [count >> 8, count & 0xffff])






# MODBUS register definitons.
register_definitions = {
    # Coils (0x) - Single bit output (Read/Write).
    "COILS": {
        "DO0": { "register": DO0_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO1": { "register": DO1_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO2": { "register": DO2_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        "DO3": { "register": DO3_ADD, "len": 1, "val": 0, "on_set_cb": dout_set_cb },
        
        "COUNT1_EN": { "register": COUNT1_EN_ADD, "len": 1, "val": 0, "on_set_cb": counter_en_set_cb },
        "COUNT3_EN": { "register": COUNT3_EN_ADD, "len": 1, "val": 0, "on_set_cb": counter_en_set_cb },
        "COUNT5_EN": { "register": COUNT5_EN_ADD, "len": 1, "val": 0, "on_set_cb": counter_en_set_cb },
        "COUNT7_EN": { "register": COUNT7_EN_ADD, "len": 1, "val": 0, "on_set_cb": counter_en_set_cb },
        "COUNT9_EN": { "register": COUNT9_EN_ADD, "len": 1, "val": 0, "on_set_cb": counter_en_set_cb },
        
        "COUNT1_RST": { "register": COUNT1_RST_ADD, "len": 1, "val": 0, "on_set_cb": counter_rst_set_cb },
        "COUNT3_RST": { "register": COUNT3_RST_ADD, "len": 1, "val": 0, "on_set_cb": counter_rst_set_cb },
        "COUNT5_RST": { "register": COUNT5_RST_ADD, "len": 1, "val": 0, "on_set_cb": counter_rst_set_cb },
        "COUNT7_RST": { "register": COUNT7_RST_ADD, "len": 1, "val": 0, "on_set_cb": counter_rst_set_cb },
        "COUNT9_RST": { "register": COUNT9_RST_ADD, "len": 1, "val": 0, "on_set_cb": counter_rst_set_cb },
    },
    
    
    # Contacts / Discrete Input (1x) - Single bit input (Read only).
    "ISTS": {
        "DI0":  { "register": DI0_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI1":  { "register": DI1_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI2":  { "register": DI2_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI3":  { "register": DI3_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI4":  { "register": DI4_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI5":  { "register": DI5_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI6":  { "register": DI6_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI7":  { "register": DI7_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI8":  { "register": DI8_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI9":  { "register": DI9_ADD,  "len": 1, "val": 0, "on_get_cb": din_get_cb },
        "DI10": { "register": DI10_ADD, "len": 1, "val": 0, "on_get_cb": din_get_cb }
    },
    
    
    # Input Registers (3x) - 16-bit input (Read only).
    "IREGS": {
        "ANV0": { "register": ANV0_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANV1": { "register": ANV1_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANA0": { "register": ANA0_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        "ANA1": { "register": ANA1_ADD, "len": 1, "val": 0, "on_get_cb": an_get_cb },
        
        "COUNT1": { "register": COUNT1_H_ADD, "len": 2, "val": [0, 0], "on_get_cb": counter_get_cb },
        "COUNT3": { "register": COUNT3_H_ADD, "len": 2, "val": [0, 0], "on_get_cb": counter_get_cb },
        "COUNT5": { "register": COUNT5_H_ADD, "len": 2, "val": [0, 0], "on_get_cb": counter_get_cb },
        "COUNT7": { "register": COUNT7_H_ADD, "len": 2, "val": [0, 0], "on_get_cb": counter_get_cb },
        "COUNT9": { "register": COUNT9_H_ADD, "len": 2, "val": [0, 0], "on_get_cb": counter_get_cb },
        
        "MODEL":   { "register": MODEL1_ADD,        "len": 2, "val": [MODEL1, MODEL2]                              },
        "VERSION": { "register": VERSION_MAJOR_ADD, "len": 3, "val": [VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH] }
    }
    
    
#     # Holding Registers (4x) - 16-bit data (Read/Write).
#     "HREGS": {
#         
#     }
}



# use the defined values of each register type provided by register_definitions
client.setup_registers(registers = register_definitions)
