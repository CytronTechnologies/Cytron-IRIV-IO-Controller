import board
import time
import iriv_ioc_modbus



while True:
    try:
        result = iriv_ioc_modbus.client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping RTU client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))