# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 16:58:51 2017

@author: Robyn.Pritchard
"""
from enum import Enum
import copy
import configparser as confp
import numpy as np
from FPGA_control_modbus_tk import FPGA_registers, FPGASettingsInfo, FPGA_params


class SettingInfo():
    def __init__(self, value, save = False, save_section = '', save_name = '', error_message = '', settings_window = False,  window_group = '', limits = [0,0]):
        self.value = value
        self.save = save
        self.save_section = save_section
        self.save_name = save_name
        self.error_message = error_message 
        self.settings_window = settings_window
        self.window_group = window_group
        self.limits = limits

class counts(object):
    
    def __init__(self):
        self.iframe = int(0)
        self.sort_num = int(0)
        self.valid_frame = int(0)
        self.total_beads = int(0)
        
    def reset(self):
        self.iframe = int(0)
        self.sort_num = int(0)
        self.valid_frame = int(0)
        self.total_beads = int(0)
        
    def print_str(self):
        print('final sort percentage was ',int((self.sort_num/self.valid_frame)*100), '% over ', self.valid_frame, 'good frames, with ', self.iframe, ' total frames' )
       
    def disp_str(self):
        out_str = 'SORTED = ' + str(int(self.sort_num)) + ' IN ' + str(int(self.valid_frame)) + ' GOOD FRAMES (' + str(int((self.sort_num/self.valid_frame)*100)) + ' %), TOTAL FRAMES = ' + str(int(self.iframe)) 
        return out_str
        

class settings:
    
    def __init__(self):
        Save = True
        Save_window = True
        self.general  =  {'LOAD_VIDEO':       SettingInfo(True, Save, 'Camera Settings', 'Load Video', 'Failed to load Camera Settings - Load Video. Setting to default value of True'),
                          'CAMERA_NUMBER':    SettingInfo(1, Save, 'Camera Settings', 'Camera Number', 'Failed to load Camera Settings - Camera Number. Setting to default value of 1', Save_window, 'Camera Settings'),
                          'CAMX':             SettingInfo(600, Save, 'Camera Settings', 'x pixels', 'Failed to load Camera Sttings - x pixels. Setting to default value of 600', Save_window, 'Camera Settings'),
                          'CAMY':             SettingInfo(1100, Save, 'Camera Settings', 'y pixels', 'Failed to load Camera Sttings - y pixels. Setting to default value of 1100', Save_window, 'Camera Settings'),
                          'SETCAMERA':        SettingInfo(True, Save, 'Camera Settings', 'Set Camera Settings', 'Failed to load Camera Settings - Set Camera Settings. Setting to default value of True'),
                          'AUTOALIGN':        SettingInfo(True, Save, 'Image Processing Settings', 'Autoalign', 'Failed to load Image Processing Settings - Autoalign. Setting to default value of True', Save_window, 'Image Processing Settings'),
                          'CROP':             SettingInfo(True, Save, 'Image Processing Settings', 'Crop', 'Failed to load Image Processing Settings - Crop. Setting to default value of True', Save_window, 'Image Processing Settings'),
                          'ROTATE_FLIP':      SettingInfo(True, Save, 'Image Processing Settings', 'Rotate and Crop', 'Failed to load Image Processing Settings - Rotate and Flip. Setting to default value of True', Save_window, 'Image Processing Settings'),
                          'DETECTION_ON':     SettingInfo(True, Save, 'Image Processing Settings', 'Detection on', 'Failed to load Bead Detection Settings - Detector On. Setting to default value of True', Save_window, 'Bead Detection Settings'),
                          'FILL_HOLES':       SettingInfo(True, Save, 'Image Processing Settings', 'Fill holes', 'Failed to load Bead Detection Settings - Fill holes. Setting to default vaue of False', Save_window, 'Bead Detection Settings'),
                          'SORTING_MODE':     SettingInfo(True, Save, 'Analysis Settings', 'Sorting mode', 'Failed to load Analysis Settings - Sorting Mode. Setting to default value of True'),
                          'RECORD':           SettingInfo(False, Save, 'Display and Recording Settings', 'Record', 'Failed to load Display and Recording Settings - Record. Setting to default value of False'),
                          'RECORD_RAW':       SettingInfo(False, Save, 'Display and Recording Settings', 'Record raw', 'Failed to load Display and Recording Settings - Record raw. Setting to default value of False' ),
                          'DRAW_ROIS':        SettingInfo(True, Save, 'Display and Recording Settings', 'Draw ROIs', 'Failed to load Display and Recording Settings - Draw ROIs. Setting to default value of True'),
                          'VALIDATION_ON':    SettingInfo(False, Save, 'Display and Recording Settings', 'Validation On', 'Failed to load Display and Recording Settings - Validation On. Setting to default value of False'),
                          'STATIONARY_ON':    SettingInfo(True),
                          'ALIGNED':          SettingInfo(False),
                          'STEPPING_MODE':    SettingInfo(False),
                          'MASKS_ON':         SettingInfo(False),
                          'FULL_WINDOW':      SettingInfo(False),
                          'UPDATE_SETTINGS':  SettingInfo(False),
                          'FRAME_SIZE':       SettingInfo([0,0]),
                          'FRAME_SIZE_RAW':   SettingInfo([0,0]),
                          'RUNNING':          SettingInfo(False),
                          'SUB_BACKGROUND':   SettingInfo(False),
                          'ITEM_LOADED':      SettingInfo(False),       
                          'FPGA_NUMBER':      SettingInfo(16, Save, 'FPGA General Settings', 'Number of FPGAs', 'Failed to load FPGA General Settings - Number of FPGAs'),
                          'FPGA_CONNECTED':   SettingInfo(False),
                          'CURRENT_FPGA':     SettingInfo(1, Save, 'FPGA General Settings', 'Current FPGA', 'Failed to load FPGA General Settings - Current FPGA'),
                         }
        
        self.detection = {'DECAY':        SettingInfo(0.05, Save, 'Bead Detection Settings', 'Decay', 'Failed to load Bead Detection Settings - Decay. Setting to default value of 0.05'),
                          'SORTPOINTS':   SettingInfo(0),
                          'WASTEPOINTS':  SettingInfo(0),
                          'DS':           SettingInfo(0),
                          'CX':           SettingInfo(0),
                          'CY':           SettingInfo(0),
                          'XOFF':         SettingInfo(0),
                          'YOFF':         SettingInfo(0),
                          'ANGLE':        SettingInfo(0),
                          'ROI':          SettingInfo(np.int64([0, 0, 640, 480])),
                          'MIN_AREA':     SettingInfo(20, Save, 'Bead Detection Settings', 'Min Bead Area', 'Failed to load Bead Detection Settings - Min Bead area. Setting to default vaue of 20'),
                          'MAX_AREA':     SettingInfo(125, Save, 'Bead Detection Settings', 'Max Bead Area', 'Failed to load Bead Detection Setting - Max Bead area. Setting to default value of 125'),
                          'MIN_THRESH':   SettingInfo(190, Save, 'Bead Detection Settings', 'Min Threshold', 'Failed to load Bead Detection Settings - Min Thresh. Setting to default vaue of 190'),
                          'MAX_THRESH':   SettingInfo(255, Save, 'Bead Detection Settings', 'Max Threshold', 'Failed to load Bead Detection Settings - Max Thresh. Setting to default vaue of 255'),
                          'BEAD_CIRC':    SettingInfo(0.6, Save, 'Bead Detection Settings', 'Min bead circulariy', 'Failed to load Bead Detection Settings - Bead Circularity. Setting to default value of 0.6'),
                          'SROI':         SettingInfo(0),
                          'SBROI':        SettingInfo(0),
                         }
            
        self.FPGAsets = np.ndarray((self.general['FPGA_NUMBER'].value), dtype = object)

        for i in np.arange(0, self.general['FPGA_NUMBER'].value):
            self.FPGAsets[i] = FPGA_params(i+1)

    
    def __copy__(self):
        return copy.deepcopy(self)  

    def save_configs(self):
        
        config = confp.ConfigParser()
        
        config.add_section('Camera Settings')
        config.add_section('Image Processing Settings')
        config.add_section('Analysis Settings')
        config.add_section('Display and Recording Settings')
        config.add_section('Bead Detection Settings')
        config.add_section('FPGA General Settings')
        
        for _, setting in self.general.items():
            if setting.save:
                if type(setting.value) == float:
                    config.set(setting.save_section, setting.save_name, '%.2f' % setting.value)
                else:
                    config.set(setting.save_section, setting.save_name, str(setting.value))
                    
        for _, setting in self.detection.items():
            if setting.save:
                if type(setting.value) == float:
                    config.set(setting.save_section, setting.save_name, '%.2f' % setting.value)
                else:
                    config.set(setting.save_section, setting.save_name, str(setting.value))
                
        for j in np.arange(0, self.general['FPGA_NUMBER'].value):
            section = 'FPGA ' + str(j+1) + ' Settings'
            config.add_section(section)
            for _, setting in self.FPGAsets[j].settings.items():
                if type(setting.value) == float:
                    config.set(section, setting.save_name, '%.2f' % setting.value)
                else:
                    config.set(section, setting.save_name, str(setting.value))
        
        with open('config.ini', 'w') as F: config.write(F)

            
    def load_configs(self):
        
        config = confp.ConfigParser()
        config.read('config.ini')
        
        for _, setting in self.general.items():
            if setting.save:
                try:
                    if type(setting.value) == bool:
                        setting.value = config.getboolean(setting.save_section, setting.save_name)
                    elif type(setting.value) == float:
                        setting.value = config.getfloat(setting.save_section, setting.save_name)
                    else:
                        setting.value = config.getint(setting.save_section, setting.save_name)
                except:
                    print(setting.error_message)
                    
        for _, setting in self.detection.items():
            if setting.save:
                try:
                    if type(setting.value) == bool:
                        setting.value = config.getboolean(setting.save_section, setting.save_name)
                    elif type(setting.value) == float:
                        setting.value = config.getfloat(setting.save_section, setting.save_name)
                    else:
                        setting.value = config.getint(setting.save_section, setting.save_name)
                except:
                    print(setting.error_message)
                    
        self.FPGAsets = np.ndarray((self.general['FPGA_NUMBER'].value), dtype = object)
        for i in np.arange(0, self.general['FPGA_NUMBER'].value):
            self.FPGAsets[i] = FPGA_params(i+1)
            
        for j in np.arange(0, self.general['FPGA_NUMBER'].value):
            section = 'FPGA ' + str(j+1) + ' Settings'
            for _, setting in self.FPGAsets[j].settings.items():
                try:
                    if type(setting.value) == bool:
                        setting.value = config.getboolean(section, setting.save_name)
                    elif type(setting.value) == float:
                        setting.value = config.getfloat(section, setting.save_name)
                    elif type(setting.value) == int:
                        setting.value = config.getint(section, setting.save_name)
                    else:
                        setting.value = config.get(section, setting.save_name)
                except:
                    print(setting.error_message + " (FPGA" +str(j+1) + ")")
                    
        self.save_configs()
        return self
         

#    def getROIs(self):
#        ''' returns [ROI,sROI,sbROI,angle]'''
#        return [self.detection.ROI, self.detection.sROI, self.detection.sbROI, self.detection.angle]
        