# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 09:04:45 2017

@author: Robyn.Pritchard
"""

import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

logger = modbus_tk.utils.create_logger("console")
master = modbus_rtu.RtuMaster(serial.Serial(port  = 'COM5', baudrate = 115200))
master.set_timeout(3.0)


while True:
        try:
            resp = master.execute(1, cst.READ_HOLDING_REGISTERS, 0x202, 1)
            print(resp[0])
        except modbus_tk.modbus.ModbusError as e:
            logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        except modbus_rtu.ModbusInvalidResponseError as e:
            logger.error("%s- Code=ModbusInvalidResponseError" % (e))
            master.close()
        except:
            logger.debug("other")

