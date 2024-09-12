# SPDX-FileCopyrightText: 2024 Wai Weng for Cytron Technologies
#
# SPDX-License-Identifier: MIT

"""
DESCRIPTION:
Example code to read the analog input for both voltage and current mode.

AUTHOR  : Wai Weng
COMPANY : Cytron Technologies Sdn Bhd
WEBSITE : www.cytron.io
EMAIL   : support@cytron.io
"""
import time
import board
import analogio

# Supply voltage (mV).
# This voltage should be around 3320 mV
SUPPLY_VOLTAGE = 3320
 
an0 = analogio.AnalogIn(board.AN0)
an1 = analogio.AnalogIn(board.AN1)
 
while True:
    # Voltage Mode (Unit = mV).
    # Make sure the AN-IN Mode switch position is "Voltage".
    print(an0.value * SUPPLY_VOLTAGE / 65536 * 16 / 5)
    
    # Current Mode (Unit = uA).
    # Make sure the AN-IN Mode switch position is "Current".
    print(an1.value * SUPPLY_VOLTAGE / 65536 * 16 / 5 / 248 * 1000)
    
    
    # Sleep for 1 second.
    time.sleep(1)