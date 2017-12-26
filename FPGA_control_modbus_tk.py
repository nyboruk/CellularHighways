# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:33:52 2017

@author: Robyn.Pritchard
"""

import image_processing_functions as ip
import numpy as np
from enum import Enum
import copy
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

class FPGA_registers(Enum):
    COMPORT = 0
    ID = 0
    BUADRATE = 0
    STROBE_NUM = 0
    FREQUENCY = 0
    ADC_BITRATE = 0
    TICK_COUNTER = 0x8
    FPGA_MODE = 0x9
    HEATER_DELAY = 0x100
    HEATER_PULSE = 0x102
    FS_THRESHOLD = 0x103
    CAM_DELAY = 0x200
    CAM_PULSE = 0x202
    STROBE_DELAY_1 = 0x203
    STROBE_DELAY_2 = 0x205
    STROBE_WIDTH = 0x207
    CAM_MIN_TRIGGER_TIME = 0x20a
    MIN_TRIGGER_TIME = 0x208
    BS_ADC_INPUT = 0x300
    BS_PGA_GAIN = 0x301
    BS_ADC_OFFSET = 0x302
    BS_ADC_CONTROL = 0x303
    FS_ADC_INPUT = 0x310
    FS_PGA_GAIN = 0x311
    FS_ADC_OFFSET = 0x312
    FS_ADC_CONTROL = 0x313
    FL_ADC_INPUT = 0x320
    FL_PGA_GAIN = 0x321
    FL_ADC_OFFSET = 0x322
    FL_ADC_CONTROL = 0x323

class FPGASettingsInfo():
    def __init__(self, value, writable, register, reg_read_num, save_section = False, save_name = '', error_message = '', convert = 0, also_write = '', settings_window = False,  window_group = '', limits = [0,0]):
        '''convert option: 0 - don't convert, 1 - convert from us to clock ticks, 2 - convert from ms to clock ticks, 3 - convert from percentage to bits'''
        self.value = value
        self.writable = writable
        self.register  = register.value
        self.reg_read_num = reg_read_num
        self.save_section = save_section
        self.save_name = save_name
        self.error_message = error_message
        self.settings_window = settings_window
        self.window_group = window_group
        self.limits = limits
        self.convert = convert
        self.also_write = also_write
 
class FPGA_params(object):
    def __init__(self, FPGA_ID_NUM):
        
        self.ID = int(FPGA_ID_NUM)
        save_section = 'FPGA ' + str(int(self.ID)) + ' Settings'
        save_window = True
        
        self.settings = {'COMPORT':          FPGASettingsInfo('COM7', False, FPGA_registers.COMPORT, 0, save_section, 'COM Port', 'Failed to load FPGA Settings - Comm Port. Setting to default value of COM7', 0, '', save_window, 'FPGA General Settings'),
                         'ID':               FPGASettingsInfo(self.ID, False, FPGA_registers.ID, 0, save_section, 'FPGA ID', 'Failed to load FPGAs - ID. Settings to default value of 0', 0, '', save_window, 'FPGA General Settings', [1, 100]),
                         'BAUDRATE':         FPGASettingsInfo(115200, False, FPGA_registers.BUADRATE, 0, save_section, 'Buadrate', 'Falied to load FPGAs - Buadrate. Setting to default value of 115200'),
                         'FREQUENCY':        FPGASettingsInfo(8000000, False, FPGA_registers.FREQUENCY, 0, save_section, 'Clock Frequency', 'Failed to load FPGAs - Clock Frequency. Settings to default value of 8Mhz.'),
                         'ADC_BITRATE':      FPGASettingsInfo(14, False, FPGA_registers.ADC_BITRATE, 1, save_section, 'ADC bitrate', 'Failed to load FPGAs - ADC bitrate. Setting to default value of 14bits.'),
                         'FPGA_MODE':        FPGASettingsInfo(0, True, FPGA_registers.FPGA_MODE, 1, save_section, 'FPGA running mode', 'Faluled to load FPGAs - Running mode. Setting to default value of 1'),
                         'HEATER_DELAY':     FPGASettingsInfo(110.0, True, FPGA_registers.HEATER_DELAY, 2, save_section, 'heater delay [us]', 'Failed to load FPGA Settings - Heater delay. Setting to default value of 210', 1, 'MIN_TRIGGER_TIME', save_window, 'FPGA ID Settings'),
                         'HEATER_PULSE':     FPGASettingsInfo(3.0, True, FPGA_registers.HEATER_PULSE, 1, save_section, 'heater pulse [us]', 'Failed to load FPGA Settings - Heater Pulse. Setting to default value of 3.0', 1, 'MIN_TRIGGER_TIME', save_window, 'FPGA ID Settings'),
                         'FS_THRESHOLD':     FPGASettingsInfo(50.0, True, FPGA_registers.FS_THRESHOLD, 1, save_section, 'FS Threshold', 'Failed to load FPGA Settings - FS Threshold. Setting to default value of 50.0', 3, '', save_window, 'FPGA ID Settings'),
                         'CAM_DELAY':        FPGASettingsInfo(100.0, True, FPGA_registers.CAM_DELAY, 2, save_section, 'Camera delay [us]', 'Failed to load FPGA Settings - Camerea delay. Setting to default value of 100', 1, 'CAM_MIN_TRIGGER_TIME', save_window, 'FPGA ID Settings'),
                         'CAM_PULSE':        FPGASettingsInfo(100.0, True, FPGA_registers.CAM_PULSE, 1, save_section, 'Camera pulse width [us]', 'Failed to load FPGA Settings - Camerea delay. Setting to default value of 100', 1, 'CAM_MIN_TRIGGER_TIME', save_window, 'FPGA ID Settings'),
                         'STROBE_NUM':       FPGASettingsInfo(2, True, FPGA_registers.STROBE_NUM, 0, save_section, 'Number of Strobes', 'Failed to load FPGA Settings - Number of strobes. Setting to default value of 2', 0),
                         'STROBE_DELAY_1':   FPGASettingsInfo(115.0, True, FPGA_registers.STROBE_DELAY_1, 2, save_section, 'Strobe delay 1 [us]', 'Failed to load FPGA Settings - Strobe delay 1. Setting to default value of 115', 1, '', save_window, 'FPGA ID Settings'),
                         'STROBE_DELAY_2':   FPGASettingsInfo(515.0, True, FPGA_registers.STROBE_DELAY_2, 2, save_section, 'Strobe delay 2 [us]', 'Failed to load FPGA Settings - Strobe delay 2. Setting to default value of 515', 1, '', save_window, 'FPGA ID Settings'),
                         'STROBE_WIDTH':     FPGASettingsInfo(1.0, True, FPGA_registers.STROBE_WIDTH, 1, save_section, 'Strobe width [us]', 'Failed to load FPGA Settings - Stobe Separation. Setting to default value of 1.0', 1, '', save_window, 'FPGA ID Settings'),
                         'MIN_TRIGGER_TIME': FPGASettingsInfo(1.0, True, FPGA_registers.MIN_TRIGGER_TIME, 2, save_section, 'Minimum trigger time [ms]', 'Failed to load FPGA Settings - minimum trigger period. Setting to default value of 25.', 4, '', save_window, 'FPGA ID Settings'),
                         'CAM_MIN_TRIGGER_TIME': FPGASettingsInfo(25.0, True, FPGA_registers.CAM_MIN_TRIGGER_TIME, 2, save_section, 'Camera Minimum trigger time [ms]', 'Failed to load FPGA settings - camera minimum trigger period. setting to default value of 25.', 5, '', save_window, 'FPGA ID Settngs'),
                         'BS_ADC_INPUT':     FPGASettingsInfo(55, False, FPGA_registers.BS_ADC_INPUT, 1, save_section, 'BS ADC Input','Failed to load FPGA Settings - BS ADC Input. Setting to default value of 55', 0),
                         'BS_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.BS_PGA_GAIN, 1, save_section, 'BS PGA Gain', 'Failed to load FPGA Settings - BS PGA Gain. Setting to default value of 1', 0, '', save_window, 'FPGA ID Settings'),
                         'BS_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.BS_ADC_OFFSET, 1, save_section, 'BS ADC Offset', 'Failed to load FPGA Settings - BS ADC Offset. Setting to default vale of 0', 0),
                         'BS_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.BS_ADC_CONTROL, 1, save_section, 'BS ADC Control', 'Failed to load FPGA Settings - BS ADC Control. Setting to default vale of 4096', 0),
                         'FS_ADC_INPUT':     FPGASettingsInfo(40230, False, FPGA_registers.FS_ADC_INPUT, 1, save_section, 'FS ADC Input', 'Failed to load FPGA Settings - FS ADC Input. Setting to default value of 40230', 0),
                         'FS_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.FS_PGA_GAIN, 1, save_section, 'FS PGA Gain', 'Failed to load FPGA Settings - FS PGA Gain. Setting to default value of 1', 0, '', save_window, 'FPGA ID Settings'),
                         'FS_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.FS_ADC_OFFSET, 1, save_section, 'FS ADC Offset','Failed to load FPGA Settings - FS ADC Offset. Setting to default vale of 0', 0),
                         'FS_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.FS_ADC_CONTROL, 1, save_section, 'FS ADC Control', 'Failed to load FPGA Settings - FS ADC Control. Setting to default vale of 4096', 0),
                         'FL_ADC_INPUT':     FPGASettingsInfo(260, False, FPGA_registers.FL_ADC_INPUT, 1, save_section, 'FL ADC Input', 'Failed to load FPGA Settings - FL ADC Input. Setting to default value of 260', 0),
                         'FL_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.FL_PGA_GAIN, 1, save_section, 'FL PGA Gain', 'Failed to load FPGA Settings - FL PGA Gain. Setting to default value of 1', 0, '', save_window, 'FPGA ID Settings'),
                         'FL_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.FL_ADC_OFFSET, 1, save_section, 'FL ADC Offset', 'Failed to load FPGA Settings - FL ADC Offset. Setting to default vale of 0', 0),
                         'FL_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.FL_ADC_CONTROL, 1, save_section, 'FL ADC Control', 'Failed to load FPGA Settings - FL ADC Control. Setting to default vale of 4096', 0),                       
                        }
    
    def print_all(self):
        for key, value in self.settings.items():
            strout = key + ': ' + str(value.value)
            print(strout)
            
    def copy(self):
        return copy.deepcopy(self)


class FPGA:
    
    def __init__(self, FPGA_params_in):
        self.params = FPGA_params_in
        self.params_temp = self.params.copy()
        
        self.logger = modbus_tk.utils.create_logger("console")
        try:
            self.master = modbus_rtu.RtuMaster(serial.Serial(port  = self.params.settings['COMPORT'].value, baudrate = self.params.settings['BAUDRATE'].value))
            self.master.set_timeout(0.1)
        except modbus_tk.modbus.ModbusError as exc:
            self.logger.error("%s- Code=%d", exc, exc.get_exception_code()) 
    
    def read_write_names(self):
        for key,_ in self.params.settings.items():
            print(key)
            
    def read(self, name):
        '''Reads from FPGA, takes strings of setting name. For setting names run "FPGA.read_write_names()".'''
        if name in self.params.settings.keys():
            reg = self.params.settings[name].register
            if reg == 0:
                return self.params.settings[name].value
            else:
                try:
                    if self.params_temp.settings[name].reg_read_num == 1:
                        return self.master.execute(self.params.settings['ID'].value, cst.READ_HOLDING_REGISTERS, self.params.settings[name].register, 1)[0]
                    elif self.params_temp.settings[name].reg_read_num == 2:
                        part1 = self.master.execute(self.params.settings['ID'].value, cst.READ_HOLDING_REGISTERS, self.params.settings[name].register, 1)[0]
                        part2 = self.master.execute(self.params.settings['ID'].value, cst.READ_HOLDING_REGISTERS, self.params.settings[name].register + 1, 1)[0]
                        return [part1, part2]
                except modbus_tk.modbus.ModbusError as e:
                    self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
                except modbus_rtu.ModbusInvalidResponseError as e:
                    self.logger.error("%s- Code=ModbusInvalidResponseError" % (e))
                    self.master.close()
                except:
                    self.logger.debug("other")
        else:
            print('Incorrect entry. Valid Entries are:')
            self.read_write_names()
     
    def convert_to(self, key):
        convert = self.params.settings[key].convert
        if convert == 0:
            val = int(self.params.settings[key].value)
        elif convert == 1:
            val = int(self.params.settings[key].value*self.params.settings['FREQUENCY'].value*0.000001)
        elif convert == 2:
            val = int(self.params.settings[key].value*self.params.settings['FREQUENCY'].value*0.001)
        elif convert == 3:
            val = int(self.params.settings[key].value*0.01*(np.power(2,self.params.settings['ADC_BITRATE'].value)-1))
        elif convert == 4:
            freq = self.params_temp.settings['FREQUENCY'].value*0.001
            val = int(self.params.settings[key].value*freq) - int(self.params_temp.settings['HEATER_PULSE'].value*freq*0.001) - int(self.params_temp.settings['HEATER_DELAY'].value*freq*0.001) - 1
        elif convert == 5:
            freq = self.params_temp.settings['FREQUENCY'].value*0.001
            val = int(self.params.settings[key].value*freq) - int(self.params_temp.settings['CAM_PULSE'].value*freq*0.001) - int(self.params_temp.settings['CAM_DELAY'].value*freq*0.001) - 1
            
        if self.params_temp.settings[key].reg_read_num == 1:
            val_arr = val
        elif self.params_temp.settings[key].reg_read_num == 2:
            binary = np.binary_repr(val,32)
            val_arr = [int(binary[0:16],2), int(binary[16:32],2)]
        return val_arr
    
    def write(self, setting, key):
        print(key)
        if self.params_temp.settings[key].reg_read_num == 1: 
            self.logger.info(self.master.execute(self.params_temp.settings['ID'].value, cst.WRITE_SINGLE_REGISTER, setting.register, output_value = self.convert_to(key)))
        elif self.params_temp.settings[key].reg_read_num == 2:
            self.logger.info(self.master.execute(self.params_temp.settings['ID'].value, cst.WRITE_SINGLE_REGISTER, setting.register, output_value = self.convert_to(key)[0]))
            self.logger.info(self.master.execute(self.params_temp.settings['ID'].value, cst.WRITE_SINGLE_REGISTER, setting.register+1, output_value = self.convert_to(key)[1]))
        self.params_temp.settings[key].value = setting.value
        
    def write_to_FPGA(self, Force_Write_all = False):
        '''For read names run FPGA.read_write_names()'''
        
        for key, setting in self.params.settings.items():
            if setting.register != 0 and setting.writable != False:
                if Force_Write_all == False:
                    if setting.value != self.params_temp.settings[key].value:
                        try:
                            self.write(setting, key)
                            if setting.also_write != '':
                                self.write(self.params_temp.settings[setting.also_write], setting.also_write)
                        except modbus_tk.modbus.ModbusError as e:
                            self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
                        except modbus_rtu.ModbusInvalidResponseError as e:
                            self.logger.error("%s- Code=ModbusInvalidResponseError" % (e))
                            self.master.close()
                        except:
                            self.logger.debug("other error")
                else:
                    try:
                        self.write(setting, key)
                    except modbus_tk.modbus.ModbusError as e:
                        self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
                    except modbus_rtu.ModbusInvalidResponseError as e:
                        self.logger.error("%s- Code=ModbusInvalidResponseError" % (e))
                        self.master.close()
                    except:
                        self.logger.debug("other error")
                        
    def gethandler(self):
        return self.params
    
    def disconnect(self):
        self.master.close()