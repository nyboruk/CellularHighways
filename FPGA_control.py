# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:33:52 2017

@author: Robyn.Pritchard
"""

import minimalmodbus as mmb
import image_processing_functions as ip
import numpy as np
from enum import Enum
import copy

class FPGA_registers(Enum):
    COMPORT = 0
    ID = 0
    BUADRATE = 0
    STROBE_NUM = 0
    FREQUENCY = 0
    ADC_BITRATE = 0
    TICK_COUNTER = 0x8
    HEATER_DELAY = 0x100
    HEATER_PULSE = 0x101
    FS_THRESHOLD = 0x102
    CAM_DELAY = 0x200
    CAM_PULSE = 0x201
    STROBE_DELAY_1 = 0x202
    STROBE_DELAY_2 = 0x203
    STROBE_WIDTH = 0x204
    MIN_TRIGGER_TIME = 0x205
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
    def __init__(self, value, writable, register, save_section = False, save_name = '', error_message = '', convert = 0, settings_window = False,  window_group = '', limits = [0,0]):
        '''convert option: 0 - don't convert, 1 - convert from us to clock ticks, 2 - convert from ms to clock ticks, 3 - convert from percentage to bits'''
        self.value = value
        self.writable = writable
        self.register  = register.value
        self.save_section = save_section
        self.save_name = save_name
        self.error_message = error_message
        self.settings_window = settings_window
        self.window_group = window_group
        self.limits = limits
        self.convert = convert
 
class FPGA_params(object):
    def __init__(self, FPGA_ID_NUM):
        
        self.ID = int(FPGA_ID_NUM)
        save_section = 'FPGA ' + str(int(self.ID)) + ' Settings'
        save_window = True
        
        self.settings = {'COMPORT':          FPGASettingsInfo('COM7', False, FPGA_registers.COMPORT, save_section, 'COM Port', 'Failed to load FPGA Settings - Comm Port. Setting to default value of COM7', 0, save_window, 'FPGA General Settings'),
                         'ID':               FPGASettingsInfo(self.ID, False, FPGA_registers.ID, save_section, 'FPGA ID', 'Failed to load FPGAs - ID. Settings to default value of 0', 0, save_window, 'FPGA General Settings', [1, 100]),
                         'BUADRATE':         FPGASettingsInfo(115200, False, FPGA_registers.BUADRATE, save_section, 'Buadrate', 'Falied to load FPGAs - Buadrate. Setting to default value of 115200'),
                         'FREQUENCY':        FPGASettingsInfo(8000000, False, FPGA_registers.FREQUENCY, save_section, 'Clock Frequency', 'Failed to load FPGAs - Clock Frequency. Settings to default value of 8Mhz.'),
                         'ADC_BITRATE':      FPGASettingsInfo(14, False, FPGA_registers.ADC_BITRATE, save_section, 'ADC bitrate', 'Failed to load FPGAs - ADC bitrate. Setting to default value of 14bits.'),
                         'HEATER_DELAY':     FPGASettingsInfo(110.0, True, FPGA_registers.HEATER_DELAY, save_section, 'heater delay [us]', 'Failed to load FPGA Settings - Heater delay. Setting to default value of 210', 1, save_window, 'FPGA ID Settings'),
                         'HEATER_PULSE':     FPGASettingsInfo(3.0, True, FPGA_registers.HEATER_PULSE, save_section, 'heater pulse [us]', 'Failed to load FPGA Settings - Heater Pulse. Setting to default value of 3.0', 1, save_window, 'FPGA ID Settings'),
                         'FS_THRESHOLD':     FPGASettingsInfo(50, True, FPGA_registers.FS_THRESHOLD, save_section, 'FS Threshold', 'Failed to load FPGA Settings - FS Threshold. Setting to default value of 1', 3, save_window, 'FPGA ID Settings'),
                         'CAM_DELAY':        FPGASettingsInfo(100.0, True, FPGA_registers.CAM_DELAY, save_section, 'Camera delay [us]', 'Failed to load FPGA Settings - Camerea delay. Setting to default value of 100', 1, save_window, 'FPGA ID Settings'),
                         'CAM_PULSE':        FPGASettingsInfo(100.0, True, FPGA_registers.CAM_PULSE, save_section, 'Camera pulse width [us]', 'Failed to load FPGA Settings - Camerea delay. Setting to default value of 100', 1, save_window, 'FPGA ID Settings'),
                         'STROBE_NUM':       FPGASettingsInfo(2, True, FPGA_registers.STROBE_NUM, save_section, 'Number of Strobes', 'Failed to load FPGA Settings - Number of strobes. Setting to default value of 2', 0),
                         'STROBE_DELAY_1':   FPGASettingsInfo(115.0, True, FPGA_registers.STROBE_DELAY_1, save_section, 'Strobe delay 1 [us]', 'Failed to load FPGA Settings - Strobe delay 1. Setting to default value of 115', 1, save_window, 'FPGA ID Settings'),
                         'STROBE_DELAY_2':   FPGASettingsInfo(515.0, True, FPGA_registers.STROBE_DELAY_2, save_section, 'Strobe delay 2 [us]', 'Failed to load FPGA Settings - Strobe delay 2. Setting to default value of 515', 1, save_window, 'FPGA ID Settings'),
                         'STROBE_WIDTH':     FPGASettingsInfo(1.0, True, FPGA_registers.STROBE_WIDTH, save_section, 'Strobe width [us]', 'Failed to load FPGA Settings - Stobe Separation. Setting to default value of 1.0', 1, save_window, 'FPGA ID Settings'),
                         'MIN_TRIGGER_TIME': FPGASettingsInfo(1.0, True, FPGA_registers.MIN_TRIGGER_TIME, save_section, 'Minimum trigger time [us]', 'Failed to load FPGA Settings - minimum trigger period. Setting to default value of 25.', 2, save_window, 'FPGA ID Settings'),
                         'BS_ADC_INPUT':     FPGASettingsInfo(55, False, FPGA_registers.BS_ADC_INPUT, save_section, 'BS ADC Input','Failed to load FPGA Settings - BS ADC Input. Setting to default value of 55', 0),
                         'BS_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.BS_PGA_GAIN, save_section, 'BS PGA Gain', 'Failed to load FPGA Settings - BS PGA Gain. Setting to default value of 1', 0, save_window, 'FPGA ID Settings'),
                         'BS_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.BS_ADC_OFFSET, save_section, 'BS ADC Offset', 'Failed to load FPGA Settings - BS ADC Offset. Setting to default vale of 0', 0),
                         'BS_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.BS_ADC_CONTROL, save_section, 'BS ADC Control', 'Failed to load FPGA Settings - BS ADC Control. Setting to default vale of 4096', 0),
                         'FS_ADC_INPUT':     FPGASettingsInfo(40230, False, FPGA_registers.FS_ADC_INPUT, save_section, 'FS ADC Input', 'Failed to load FPGA Settings - FS ADC Input. Setting to default value of 40230', 0),
                         'FS_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.FS_PGA_GAIN, save_section, 'FS PGA Gain', 'Failed to load FPGA Settings - FS PGA Gain. Setting to default value of 1', 0, save_window, 'FPGA ID Settings'),
                         'FS_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.FS_ADC_OFFSET, save_section, 'FS ADC Offset','Failed to load FPGA Settings - FS ADC Offset. Setting to default vale of 0', 0),
                         'FS_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.FS_ADC_CONTROL, save_section, 'FS ADC Control', 'Failed to load FPGA Settings - FS ADC Control. Setting to default vale of 4096', 0),
                         'FL_ADC_INPUT':     FPGASettingsInfo(260, False, FPGA_registers.FL_ADC_INPUT, save_section, 'FL ADC Input', 'Failed to load FPGA Settings - FL ADC Input. Setting to default value of 260', 0),
                         'FL_PGA_GAIN':      FPGASettingsInfo(1.0, True, FPGA_registers.FL_PGA_GAIN, save_section, 'FL PGA Gain', 'Failed to load FPGA Settings - FL PGA Gain. Setting to default value of 1', save_window, 'FPGA ID Settings', 0),
                         'FL_ADC_OFFSET':    FPGASettingsInfo(0, True, FPGA_registers.FL_ADC_OFFSET, save_section, 'FL ADC Offset', 'Failed to load FPGA Settings - FL ADC Offset. Setting to default vale of 0', 0),
                         'FL_ADC_CONTROL':   FPGASettingsInfo(4096, True, FPGA_registers.FL_ADC_CONTROL, save_section, 'FL ADC Control', 'Failed to load FPGA Settings - FL ADC Control. Setting to default vale of 4096', 0),                       
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
        
        self.instrument = mmb.Instrument(self.params.settings['COMPORT'].value, self.params.settings['ID'].value)
        self.instrument.serial.baudrate = int(self.params.settings['BUADRATE'].value)   
    
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
                    return self.instrument.read_register(self.params.settings[name].register)
                except IOError:
                    print("Failed to read from instrument")
        else:
            print('Incorrect entry. Valid Entries are:')
            self.read_write_names()
     
    def convert_to(self, key):
        convert = self.params.settings[key].convert
        if convert == 0 or convert == 4:
            val = int(self.params.settings[key].value)
        elif convert == 1:
            val = int(self.params.settings[key].value*self.params.settings['FREQUENCY'].value*0.000001)
        elif convert == 2:
            val = int(self.params.settings[key].value*self.params.settings['FREQUENCY'].value*0.001)
        elif convert == 3:
            val = int(self.params.settings[key].value*0.01*(np.power(2,self.params.settings['ADC_BITRATE'].value)-1))
        
        return val
    
    def write_to_FPGA(self, Force_Write_all = False):
        '''For read names run FPGA.read_write_names()'''
        
        for key, setting in self.params.settings.items():
            if setting.register != 0 and setting.writable != False:
                if Force_Write_all == False:
                    if setting.value != self.params_temp.settings[key].value:
                        try:
                            self.instrument.write_register(setting.register, self.convert_to(key))
                            self.params_temp.settings[key].value = setting.value 
                            printstr = 'updated: '+ str(key)
                            print(printstr)

                        except IOError:
                            print("Failed to write/read from instrument for " + key)
                else:
                    try:
                        self.instrument.write_register(setting.register, self.convert_to(key))
                        self.params_temp.settings[key].value = setting.value
                        print(key)
                    except IOError:
                        print("Failed to write/read from instrument for " + key)
         
    def gethandler(self):
        return self.params