# SPDX-FileCopyrightText: 2024 Wai Weng for Cytron Technologies
#
# SPDX-License-Identifier: MIT

"""
DESCRIPTION:
Example code to read from a MODBUS RTU device.

AUTHOR  : Wai Weng
COMPANY : Cytron Technologies Sdn Bhd
WEBSITE : www.cytron.io
EMAIL   : support@cytron.io
"""

import board
import time
from umodbus.serial import Serial as ModbusRTUMaster

# RTU Host/Master setup
host = ModbusRTUMaster(
    tx_pin=board.TX,
    rx_pin=board.RX,
    # baudrate=9600,        # optional, default 9600
    # data_bits=8,          # optional, default 8
    # stop_bits=1,          # optional, default 1
    # parity=None,          # optional, default None
)

while True:
    data = host.read_holding_registers(slave_addr=1, starting_addr=0, register_qty=2, signed=False)
    print('Status: {}'.format(data))
    time.sleep(0.5)