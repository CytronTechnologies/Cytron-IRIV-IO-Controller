import board
import time
import iriv_ioc_modbus
import iriv_ioc_hal as Hal



timestamp = time.monotonic()

while True:
    try:
        result = iriv_ioc_modbus.client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping RTU client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))
    
    # Blink LED.
    if (time.monotonic() - timestamp >= 0.5):
        timestamp = time.monotonic()
        Hal.led.value ^= 1