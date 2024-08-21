# SPDX-FileCopyrightText: 2024 Wai Weng for Cytron Technologies
#
# SPDX-License-Identifier: MIT

"""
DESCRIPTION:
Example code to use the digital inputs as counter.

AUTHOR  : Wai Weng
COMPANY : Cytron Technologies Sdn Bhd
WEBSITE : www.cytron.io
EMAIL   : support@cytron.io
"""

import board
import digitalio
import countio
import time

# Counter is only available on DI1, DI3, DI5, DI7 and DI9.
# Count the falling edge.
count1 = countio.Counter(board.DI1, edge=countio.Edge.FALL)
count3 = countio.Counter(board.DI3, edge=countio.Edge.FALL)
count5 = countio.Counter(board.DI5, edge=countio.Edge.FALL)
count7 = countio.Counter(board.DI7, edge=countio.Edge.FALL)
count9 = countio.Counter(board.DI9, edge=countio.Edge.FALL)

# Reset the counters.
count1.reset()
count3.reset()
count5.reset()
count7.reset()
count9.reset()


while True:
    # Print out the counter value.
    print(count1.count, count3.count, count5.count, count7.count, count9.count)
    
    # Sleep for 1 second.
    time.sleep(1)