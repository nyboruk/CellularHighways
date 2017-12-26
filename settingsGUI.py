# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 21:12:06 2017

@author: Robyn.Pritchard
"""
import tkinter as tk
from tkinter import ttk
from tkinter import *
import image_processing_functions as ip
import numpy as np
from SettingsClasses import *

class SettingsPopUp:
    def __init__(self, parent, settings):
        self.settings = settings
        top = self.top = tk.Toplevel(parent)
        self.top.resizable(0,0)
        self.top.protocol("WM_DELETE_WINDOW", self.Exit)

        self.setsMainFrame = tk.Frame(self.top, width = 600, height = 500)
        self.setsMainFrame.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        self.settingsFrame = LabelFrame(self.setsMainFrame, text = 'Settings', font = "Consolas 12 bold")
        self.settingsFrame.grid(row = 0, column = 0, ipadx = 5, ipady = 5, sticky = 'news')
        
        '''Camera Settings'''
        ent_width = int(10)
        self.CameraSettings = LabelFrame(self.settingsFrame, text = "Camera Settings", font = "Consolas 10 bold")
        self.CameraSettings.grid(row = 0, column = 0, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)
        
        Label_cam_num = Label(self.CameraSettings, text = "Camera port: ").grid(row = 0, column = 0, sticky = E)
        self.Entry_cam_num = Entry(self.CameraSettings, width = ent_width)
        self.Entry_cam_num.grid(row = 0, column = 1)
        
        Label_cam_x = Label(self.CameraSettings, text = "x pixel size: ").grid(row = 1, column = 0, sticky = E)
        self.Entry_cam_x = Entry(self.CameraSettings, width = ent_width)
        self.Entry_cam_x.grid(row = 1, column = 1)
        
        Label_cam_y = Label(self.CameraSettings, text = "y pixel size: ").grid(row = 2, column = 0, sticky = E)
        self.Entry_cam_y = Entry(self.CameraSettings, width = ent_width)
        self.Entry_cam_y.grid(row = 2, column = 1)
        
        '''Image Processing Settings'''
        self.ImageProcessSets = LabelFrame(self.settingsFrame, text = "Image Processing Settings", font = "Consolas 10 bold")
        self.ImageProcessSets.grid(row = 1, column = 0, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)
        
        self.CheckBox_Autoalign_var = BooleanVar()
        self.CheckBox_Autoalign = Checkbutton(self.ImageProcessSets, text = "Autoalign ON/OFF", variable = self.CheckBox_Autoalign_var)
        self.CheckBox_Autoalign.grid(row = 0, column = 0, columnspan = 2, sticky = W)
        
        self.CheckBox_Crop_var = BooleanVar()
        self.CheckBox_Crop = Checkbutton(self.ImageProcessSets, text = "Cropping ON/OFF", variable = self.CheckBox_Crop_var)
        self.CheckBox_Crop.grid(row = 1, column = 0, columnspan = 2, sticky = W)
        
        self.CheckBox_Rotate_var = BooleanVar()
        self.CheckBox_Rotate = Checkbutton(self.ImageProcessSets, text = "Rotate and Flip ON/OFF", variable = self.CheckBox_Rotate_var)
        self.CheckBox_Rotate.grid(row = 2, column = 0, columnspan = 2, sticky = W)
        
        
        '''Bead detection Settings'''
        
        self.DetectionSets = LabelFrame(self.settingsFrame, text = "Bead Detection Settings", font = "Consolas 10 bold")
        self.DetectionSets.grid(row = 2, column = 0, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)        
        detectrow = int(0)
        
        self.Checkbox_detection_on_var = BooleanVar()
        self.Checkbox_detection_on = Checkbutton(self.DetectionSets, text = "Detection ON/OFF", variable = self.Checkbox_detection_on_var)
        self.Checkbox_detection_on.grid(row = detectrow, column = 0, columnspan = 3, sticky = W)
        detectrow +=1
        
        self.CheckBox_Fillholes_var = BooleanVar()
        self.CheckBox_Fillholes = Checkbutton(self.DetectionSets, text = "Fill holes ON/OFF", variable = self.CheckBox_Fillholes_var)
        self.CheckBox_Fillholes.grid(row = detectrow, column = 0, columnspan = 3, sticky = W)
        detectrow +=1
        
        self.CheckBox_Validation_var = BooleanVar()
        self.CheckBox_Validation = Checkbutton(self.DetectionSets, text = "Validation ON/OFF", variable = self.CheckBox_Validation_var)
        self.CheckBox_Validation.grid(row = detectrow, column = 0, columnspan = 3, sticky = W)
        detectrow += 1
        ent_width1 = int(5)
        
        Label_min_max_thresh = Label(self.DetectionSets, text = "Thresholds [Min]-[Max]:").grid(row = detectrow, column = 0, sticky = E)
        self.Entry_min_thresh = Entry(self.DetectionSets, width = ent_width1)
        self.Entry_min_thresh.grid(row = detectrow, column = 1, padx = 2)
        self.Entry_max_thresh = Entry(self.DetectionSets, width = ent_width1)
        self.Entry_max_thresh.grid(row = detectrow, column = 2, padx = 2)
        detectrow +=1
        
        Label_min_max_bead_size = Label(self.DetectionSets, text = "Bead Size [Min]-[Max]:").grid(row = detectrow, column = 0, sticky = E)
        self.Entry_min_bead = Entry(self.DetectionSets, width = ent_width1)
        self.Entry_min_bead.grid(row = detectrow, column = 1, padx = 2)
        self.Entry_max_bead = Entry(self.DetectionSets, width = ent_width1)
        self.Entry_max_bead.grid(row = detectrow, column = 2, padx = 2)
        detectrow +=1
        
        Label_bead_circularity = Label(self.DetectionSets, text = "Bead Ciculariy (0-1):").grid(row = detectrow, column = 0, sticky = E)
        self.Entry_bead_circ = Entry(self.DetectionSets, width = ent_width1)
        self.Entry_bead_circ.grid(row = detectrow, column = 1)
        detectrow +=1
   
        '''Display Settings'''
        
        self.dispSets = LabelFrame(self.settingsFrame, text = "Display Settings", font = "Consolas 10 bold")
        self.dispSets.grid(row = 3, column = 0, rowspan = 1, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)
        rownum = int(0)
        
        self.Checkbox_record_raw_var = BooleanVar()
        self.Checkbox_record_raw = Checkbutton(self.dispSets, text = "Record raw footage", variable = self.Checkbox_record_raw_var)
        self.Checkbox_record_raw.grid(row = rownum, column = 0, columnspan = 2, sticky = W)
        rownum += 1
        
        self.Checkbox_show_ROIs_var = BooleanVar()
        self.Checkbox_show_ROIS = Checkbutton(self.dispSets, text = "Show ROIs", variable = self.Checkbox_show_ROIs_var)
        self.Checkbox_show_ROIS.grid(row = rownum, column = 0, columnspan = 2, sticky = W)
        rownum += 1
        
        '''FPGA general settings'''
        ent_width2 = int(10)
        rownum = 0
        
        self.FPGAgensets = LabelFrame(self.settingsFrame, text = "FPGA general Settings", font = "Consolas 10 bold")
        self.FPGAgensets.grid(row = 0, column = 1, rowspan = 1, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)
        
        Label_FPGA_port = Label(self.FPGAgensets, text = "FPGA COM Port: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FPGA_port = Entry(self.FPGAgensets, width = ent_width2)
        self.Entry_FPGA_port.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_FPGA_num = Label(self.FPGAgensets, text = "Number of FPGAs").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FPGA_number = Entry(self.FPGAgensets, width = ent_width2)
        self.Entry_FPGA_number.grid(row = rownum, column = 1)
        rownum += 1
        
        '''FPGA ID settings'''
        ent_width2 = int(10)
        rownum = 0


        self.FPGAsets = LabelFrame(self.settingsFrame, text = "FPGA ID Settings", font = "Consolas 10 bold")
        self.FPGAsets.grid(row = 1, column = 1, rowspan = 3, sticky = 'news', ipadx = 5, ipady = 5, padx = 5, pady = 1)
        
        Label_FPGA_id = Label(self.FPGAsets, text = "FPGA ID: ").grid(row = rownum, column = 0, sticky = E)
        self.IDvar = StringVar()
        IDs = []
        for i in np.arange(0, self.settings.general['FPGA_NUMBER'].value):
            IDs.append(str(i+1))
        self.IDvar.set('1')
        self.IDmenu = OptionMenu(self.FPGAsets, self.IDvar, *IDs, command = self.FPGA_IDchange)
        self.IDmenu.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_FPGA_mode = Label(self.FPGAsets, text = "FPGA MODE:").grid(row= rownum, column = 0, sticky = E)
        self.ModeVar = StringVar()
        Modes = ['Test','Run','Off']
        self.ModeVar.set('Off')
        self.ModeMenu = OptionMenu(self.FPGAsets, self.ModeVar, *Modes, command = self.Mode_Change)
        self.ModeMenu.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_FPGA_min_rep = Label(self.FPGAsets, text = "Heater Min Repeat time [ms]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FPGA_min_rep = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_FPGA_min_rep.grid(row = rownum, column = 1 )
        rownum += 1
        
        Label_FPGA_cam_min_rep = Label(self.FPGAsets, text = "Camera Min Repeat time [ms]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FPGA_cam_min_rep = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_FPGA_cam_min_rep.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_heater_pulse = Label(self.FPGAsets, text = "Heater pulse [us]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_heater_pulse = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_heater_pulse.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_heater_delay = Label(self.FPGAsets, text = "Heater delay [us]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_heater_delay = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_heater_delay.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_cam_delay = Label(self.FPGAsets, text = "Camera delay [us]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_cam_delay = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_cam_delay.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_strobe_num = Label(self.FPGAsets, text = "num of strobe pulses:").grid(row = rownum, column = 0, sticky = E)
        self.Entry_strobe_num = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_strobe_num.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_strobe_width = Label(self.FPGAsets, text = "strobe width [us]").grid(row = rownum, column = 0, sticky = E)
        self.Entry_strobe_width = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_strobe_width.grid(row = rownum, column = 1)
        rownum += 1        
        
        Label_strobe_delay = Label(self.FPGAsets, text = "Strobe 1 delay [us]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_strobe_delay = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_strobe_delay.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_strobe_separation = Label(self.FPGAsets, text = "Strobe 2 delay [us]: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_strobe_separation = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_strobe_separation.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_FS_Threshold = Label(self.FPGAsets, text = "FS Threshold: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FS_Threshold = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_FS_Threshold.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_FS_gain = Label(self.FPGAsets, text = "FS gain: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FS_gain = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_FS_gain.grid(row = rownum, column = 1)
        rownum += 1
        
        Label_BS_gain = Label(self.FPGAsets, text = "BS gain: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_BS_gain = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_BS_gain.grid(row = rownum, column  = 1)
        rownum += 1
        
        Label_FL_gain = Label(self.FPGAsets, text = "FL gain: ").grid(row = rownum, column = 0, sticky = E)
        self.Entry_FL_gain = Entry(self.FPGAsets, width = ent_width2)
        self.Entry_FL_gain.grid(row = rownum, column = 1)
        rownum += 1
        
        self.CheckBox_FPGA_set_all_var = BooleanVar()
        self.CheckBox_FPGA_set_all = Checkbutton(self.FPGAsets, text = "Apply settings to all FPGAs", variable = self.CheckBox_FPGA_set_all_var)
        self.CheckBox_FPGA_set_all.grid(row = rownum, column = 0, columnspan = 2, sticky = W)
        rownum +=1
        
        '''buttons'''
        
        self.ok_btn = Button(self.settingsFrame, text = "Set Settings", width = 20, command = self.okay)
        self.ok_btn.grid(row = 4, column = 0, columnspan = 1, sticky = 'E', padx = 10, pady = 10)
        self.ok_btn.config(relief = "raised", background = 'pale green')
        
        self.cancel_btn = Button(self.settingsFrame, text = "Cancel", width = 20, command = self.Exit)
        self.cancel_btn.grid(row = 4, column = 1, columnspan = 1, sticky = 'W', padx = 10, pady = 10)
        self.cancel_btn.config(relief = "raised", background = 'tomato')
        
        
        '''load in the settings'''
        self.load_settings()

    def load_settings(self):
        
        #camera number
        self.Entry_cam_num.delete(0,END)
        self.Entry_cam_num.insert(0,str(int(self.settings.general['CAMERA_NUMBER'].value)))
        
        #camera x and y pixel
        self.Entry_cam_x.delete(0, END)
        self.Entry_cam_y.delete(0, END)
        self.Entry_cam_x.insert(0,str(int(self.settings.general['CAMX'].value)))
        self.Entry_cam_y.insert(0,str(int(self.settings.general['CAMY'].value)))
        
        #image processing check boxes
        if self.settings.general['AUTOALIGN'].value:
            self.CheckBox_Autoalign.select()
        else:
            self.CheckBox_Autoalign.deselect()
        
        if self.settings.general['CROP'].value:
            self.CheckBox_Crop.select()
        else:
            self.CheckBox_Crop.deselect()
            
        if self.settings.general['ROTATE_FLIP'].value:
            self.CheckBox_Rotate.select()
        else:
            self.CheckBox_Rotate.deselect()  
        
        #detection check box
        if self.settings.general['DETECTION_ON'].value:
            self.Checkbox_detection_on.select()
        else:
            self.Checkbox_detection_on.deselect()
            
        if self.settings.general['FILL_HOLES'].value:
            self.CheckBox_Fillholes.select()
        else:
            self.CheckBox_Fillholes.deselect()
        
        if self.settings.general['VALIDATION_ON'].value:
            self.CheckBox_Validation.select()
        else:
            self.CheckBox_Validation.deselect()
            
        #display setting checkboxes
        if self.settings.general['RECORD_RAW'].value:
            self.Checkbox_record_raw.select()
        else:
            self.Checkbox_record_raw.deselect()
            
        if self.settings.general['DRAW_ROIS'].value:
            self.Checkbox_show_ROIS.select()
        else:
            self.Checkbox_show_ROIS.deselect()
            
            

        
        #detection settings
        self.Entry_min_thresh.delete(0, END)
        self.Entry_max_thresh.delete(0, END)
        self.Entry_min_bead.delete(0, END)
        self.Entry_max_bead.delete(0, END)
        self.Entry_bead_circ.delete(0, END)
        
        self.Entry_min_thresh.insert(0, str(int(self.settings.detection['MIN_THRESH'].value)))
        self.Entry_max_thresh.insert(0, str(int(self.settings.detection['MAX_THRESH'].value)))
        self.Entry_min_bead.insert(0, str(int(self.settings.detection['MIN_AREA'].value)))
        self.Entry_max_bead.insert(0, str(int(self.settings.detection['MAX_AREA'].value)))
        self.Entry_bead_circ.insert(0, '%.1f' % self.settings.detection['BEAD_CIRC'].value)

        #FPGA settings
        self.Entry_FPGA_port.delete(0, END)
        self.Entry_FPGA_number.delete(0, END)
        self.Entry_FPGA_min_rep.delete(0, END)
        self.Entry_FPGA_cam_min_rep.delete(0,END)
        self.Entry_heater_pulse.delete(0, END)
        self.Entry_heater_delay.delete(0, END)
        self.Entry_cam_delay.delete(0, END)
        self.Entry_strobe_num.delete(0, END)
        self.Entry_strobe_width.delete(0, END)
        self.Entry_strobe_delay.delete(0, END)
        self.Entry_strobe_separation.delete(0, END)
        self.Entry_FS_Threshold.delete(0, END)
        self.Entry_FS_gain.delete(0, END)
        self.Entry_BS_gain.delete(0, END)
        self.Entry_FL_gain.delete(0, END)
        
        self.Entry_FPGA_port.insert(0, self.settings.FPGAsets[0].settings['COMPORT'].value)
        self.Entry_FPGA_number.insert(0, str(int(self.settings.general['FPGA_NUMBER'].value)))
        self.Entry_FPGA_min_rep.insert(0, '%.2f' % self.settings.FPGAsets[0].settings['MIN_TRIGGER_TIME'].value)
        self.Entry_FPGA_cam_min_rep.insert(0, '%.2f' % self.settings.FPGAsets[0].settings['CAM_MIN_TRIGGER_TIME'].value)
        self.Entry_heater_pulse.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['HEATER_PULSE'].value)
        self.Entry_heater_delay.insert(0, '%.1f' %  self.settings.FPGAsets[0].settings['HEATER_DELAY'].value)
        self.Entry_cam_delay.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['CAM_DELAY'].value)
        self.Entry_strobe_num.insert(0, str(int(self.settings.FPGAsets[0].settings['STROBE_NUM'].value)))
        self.Entry_strobe_width.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['STROBE_WIDTH'].value)
        self.Entry_strobe_delay.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['STROBE_DELAY_1'].value)
        self.Entry_strobe_separation.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['STROBE_DELAY_2'].value)
        self.Entry_FS_Threshold.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['FS_THRESHOLD'].value)
        self.Entry_FS_gain.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['FS_PGA_GAIN'].value)
        self.Entry_BS_gain.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['BS_PGA_GAIN'].value)
        self.Entry_FL_gain.insert(0, '%.1f' % self.settings.FPGAsets[0].settings['FL_PGA_GAIN'].value)      

        mode = self.settings.FPGAsets[0].settings['FPGA_MODE'].value
        if mode == 1:
            self.ModeMenu.configure()
            self.ModeVar.set('Test')
        elif mode == 2:
            self.ModeVar.set('Run')
        else:
            self.ModeVar.set('Off')
            self.settings.FPGAsets[0].settings['FPGA_MODE'].value = 0
        
        if self.settings.general['RUNNING'].value:
            self.disable()       
        
    

    def FPGA_IDchange(self, var):
        ID = int(var)
        self.settings.general['CURRENT_FPGA'].value = ID
        
        self.Entry_FPGA_min_rep.delete(0, END)
        self.Entry_FPGA_cam_min_rep.delete(0,END)
        self.Entry_heater_pulse.delete(0, END)
        self.Entry_heater_delay.delete(0, END)
        self.Entry_cam_delay.delete(0, END)
        self.Entry_strobe_num.delete(0, END)
        self.Entry_strobe_width.delete(0, END)
        self.Entry_strobe_delay.delete(0, END)
        self.Entry_strobe_separation.delete(0, END)
        self.Entry_FS_Threshold.delete(0, END)
        self.Entry_FS_gain.delete(0, END)
        self.Entry_BS_gain.delete(0, END)
        self.Entry_FL_gain.delete(0, END)
        
        self.Entry_FPGA_min_rep.insert(0, '%.2f' % self.settings.FPGAsets[ID-1].settings['MIN_TRIGGER_TIME'].value)
        self.Entry_FPGA_cam_min_rep.insert(0, '%.2f' % self.settings.FPGAsets[0].settings['CAM_MIN_TRIGGER_TIME'].value)
        self.Entry_heater_pulse.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['HEATER_PULSE'].value)
        self.Entry_heater_delay.insert(0, '%.1f' %  self.settings.FPGAsets[ID-1].settings['HEATER_DELAY'].value)
        self.Entry_cam_delay.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['CAM_DELAY'].value)
        self.Entry_strobe_num.insert(0, str(int(self.settings.FPGAsets[ID-1].settings['STROBE_NUM'].value)))
        self.Entry_strobe_width.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['STROBE_WIDTH'].value)
        self.Entry_strobe_delay.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['STROBE_DELAY_1'].value)
        self.Entry_strobe_separation.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['STROBE_DELAY_2'].value)
        self.Entry_FS_Threshold.insert(0, '%.1f' % self.settings.FPGAsets[ID-1].settings['FS_THRESHOLD'].value)
        self.Entry_FS_gain.insert(0, '%.1f' %self.settings.FPGAsets[ID-1].settings['FS_PGA_GAIN'].value)
        self.Entry_BS_gain.insert(0, '%.1f' %self.settings.FPGAsets[ID-1].settings['BS_PGA_GAIN'].value)
        self.Entry_FL_gain.insert(0, '%.1f' %self.settings.FPGAsets[ID-1].settings['FL_PGA_GAIN'].value)       
        
        mode = self.settings.FPGAsets[ID-1].settings['FPGA_MODE'].value
        if mode == 1:
            self.ModeVar.set('Test')
        elif mode == 'Run':
            self.ModeVar.set('Run')
        else:
            self.ModeVar.set('Off')
            self.settings.FPGAsets[ID-1].settings['FPGA_MODE'].value = 0

    def Mode_Change(self, var):
        ID = self.settings.general['CURRENT_FPGA'].value
        if var == 'Test':
            self.settings.FPGAsets[ID-1].settings['FPGA_MODE'].value = 1
        elif var == 'Run':
            self.settings.FPGAsets[ID-1].settings['FPGA_MODE'].value = 2
        elif var == 'Off':
            self.settings.FPGAsets[ID-1].settings['FPGA_MODE'].value = 0
        
    def disable(self):
        self.CheckBox_Autoalign.config(state = DISABLED)
        self.CheckBox_Crop.config(state = DISABLED)
        self.CheckBox_Rotate.config(state = DISABLED)
        self.Entry_cam_num.config(state = DISABLED)
        self.Entry_cam_x.config(state = DISABLED)
        self.Entry_cam_y.config(state = DISABLED)
        
    def okay(self):

        error = False
        ### camera settings
        try:
            temp = int(float(self.Entry_cam_num.get()))
            if temp > -1:
                self.Entry_cam_num.delete(0,END)
                self.Entry_cam_num.insert(0,str(temp))
            else:
                error = True
                self.Entry_cam_num.delete(0,END)
                self.Entry_cam_num.insert(0,str(int(self.settings.general['CAMERA_NUMBER'].value)))
                print("Camera Settings must be an integer greater or equal to 0.")
        except ValueError:
            error = True
            self.Entry_cam_num.delete(0,END)
            self.Entry_cam_num.insert(0,str(int(self.settings.general['CAMERA_NUMBER'].value)))
            print("Camera Settings must be an integer greater or equal to 0.")
            
        ### camera pixels
        try:
            tempx = int(float(self.Entry_cam_x.get()))
            tempy = int(float(self.Entry_cam_y.get()))
            if tempx > 0 and tempy >0 and tempx <5000 and tempy < 5000:
                self.Entry_cam_x.delete(0, END)
                self.Entry_cam_x.insert(0,str(tempx))
                self.Entry_cam_y.delete(0, END)
                self.Entry_cam_y.insert(0,str(tempy))
            else:
                error = True
                self.Entry_cam_x.delete(0, END)
                self.Entry_cam_y.delete(0, END)
                self.Entry_cam_x.insert(0,str(int(self.settings.general['CAMX'].value)))
                self.Entry_cam_y.insert(0,str(int(self.settings.general['CAMY'].value)))
                print("Camera pixel entrys must be between 0 and 5000")
        except ValueError:
                error = True
                self.Entry_cam_x.delete(0, END)
                self.Entry_cam_y.delete(0, END)
                self.Entry_cam_x.insert(0,str(int(self.settings.general['CAMX'].value)))
                self.Entry_cam_y.insert(0,str(int(self.settings.general['CAMY'].value)))
                print("Camera pixel entrys must be between 0 and 5000")

        ### get checkboxes
        self.settings.general['AUTOALIGN'].value = self.CheckBox_Autoalign_var.get()
        self.settings.general['CROP'].value = self.CheckBox_Crop_var.get()
        self.settings.general['ROTATE_FLIP'].value = self.CheckBox_Rotate_var.get()
        self.settings.general['FILL_HOLES'].value = self.CheckBox_Fillholes_var.get()
        self.settings.general['DETECTION_ON'].value = self.Checkbox_detection_on_var.get()
        self.settings.general['DRAW_ROIS'].value = self.Checkbox_show_ROIs_var.get()
        self.settings.general['RECORD_RAW'].value = self.Checkbox_record_raw_var.get()
        self.settings.general['VALIDATION_ON'].value = self.CheckBox_Validation_var.get()
        ### threshold settings
        try:
            tempmaxthresh = int(float(self.Entry_max_thresh.get()))
            tempminthresh = int(float(self.Entry_min_thresh.get()))
            if tempmaxthresh>tempminthresh and tempminthresh>-1 and tempmaxthresh<256:
                self.Entry_min_thresh.delete(0, END)
                self.Entry_max_thresh.delete(0, END)
                self.Entry_min_thresh.insert(0, str(int(tempminthresh)))
                self.Entry_max_thresh.insert(0, str(int(tempmaxthresh)))
            else:
                error = True
                self.Entry_min_thresh.delete(0, END)
                self.Entry_max_thresh.delete(0, END)
                self.Entry_min_thresh.insert(0, str(int(self.settings.detection['MIN_THRESH'].value)))
                self.Entry_max_thresh.insert(0, str(int(self.settings.detection['MAX_THRESH'].value)))
                print("Threshold values should be between 0 and 255")
        except ValueError:
            error = True
            self.Entry_min_thresh.delete(0, END)
            self.Entry_max_thresh.delete(0, END)
            self.Entry_min_thresh.insert(0, str(int(self.settings.detection['MIN_THRESH'].value)))
            self.Entry_max_thresh.insert(0, str(int(self.settings.detection['MAX_THRESH'].value)))
            print("Threshold values should be between 0 and 255")            
                
        ### bead size settings
        try:
            tempminbead = int(float(self.Entry_min_bead.get()))
            tempmaxbead = int(float(self.Entry_max_bead.get()))
            if tempminbead < tempmaxbead and tempminbead>1 and tempmaxbead <1000:
                self.Entry_min_bead.delete(0, END)
                self.Entry_max_bead.delete(0, END)
                self.Entry_min_bead.insert(0, str(tempminbead))
                self.Entry_max_bead.insert(0, str(tempmaxbead))
            else:
                error = True
                self.Entry_min_bead.delete(0, END)
                self.Entry_max_bead.delete(0, END)
                self.Entry_min_bead.insert(0, str(int(self.settings.detection['MIN_AREA'].value)))
                self.Entry_max_bead.insert(0, str(int(self.settings.detection['MAX_AREA'].value)))
                print("Bead area must be greater than 0 and less than 1000")
        except ValueError:
            error = True
            self.Entry_min_bead.delete(0, END)
            self.Entry_max_bead.delete(0, END)
            self.Entry_min_bead.insert(0, str(int(self.settings.detection['MIN_AREA'].value)))
            self.Entry_max_bead.insert(0, str(int(self.settings.detection['MAX_AREA'].value)))
            print("Bead area must be greater than 0 and less than 1000")
        
        try:
            tempbeadcirc = float('%.2f'% float(self.Entry_bead_circ.get()))
            if tempbeadcirc > 0 and tempbeadcirc < 1:
                self.Entry_bead_circ.delete(0, END)
                self.Entry_bead_circ.insert(0, str(tempbeadcirc))
            else:
                error = True
                self.Entry_bead_circ.delete(0, END)
                self.Entry_bead_circ.insert(0, str(self.settings.detection['BEAD_CIRC'].value))
                print('Circularity must be betwee 0 and 1.')
        except ValueError:
            error = True
            self.Entry_bead_circ.delete(0, END)
            self.Entry_bead_circ.insert(0, str(self.settings.detection['BEAD_CIRC'].value))
            print('Circularity must be betwee 0 and 1.')
        
        ### FPGA Settings
        
        try:
            tempFPGAport = self.Entry_FPGA_port.get()
            if tempFPGAport[0:3] == 'COM' and int(tempFPGAport[3:]) > -1:
                self.Entry_FPGA_port.delete(0, END)
                self.Entry_FPGA_port.insert(0, tempFPGAport)
            else:
                error = True
                self.Entry_FPGA_port.delete(0, END)
                self.Entry_FPGA_port.insert(0, self.settings.FPGAsets[0].setings['COMPORT'].value)
                print('Comm port must be an integer greater than or equal to 0 and enter as "COM#"')
        except ValueError:
            error = True
            self.Entry_FPGA_num.delete(0, END)
            self.Entry_FPGA_num.insert(0, str(self.settings.FPGAsets[0].setings['COMPORT'].value))
            print('Comm port must be an integer greater than or equal to 0 and enter as "COM#"')
        
        try:
            tempFPGAnum = int(self.Entry_FPGA_number.get())
            if tempFPGAnum > 0 and tempFPGAnum <100:
                self.Entry_FPGA_number.delete(0, END)
                self.Entry_FPGA_number.insert(0, str(tempFPGAnum))
            else:
                error = True
                self.Entry_FPGA_number.delete(0, END)
                self.Entry_FPGA_number.insert(0, str(self.general['FPGA_NUMBER'].value))
                print('FPGA number must be an integer between 1 and 100.')
        except ValueError:
                error = True
                self.Entry_FPGA_number.delete(0, END)
                self.Entry_FPGA_number.insert(0, str(self.general['FPGA_NUMBER'].value))
                print('FPGA number must be an integer between 1 and 100.')

        
        var = int(self.IDvar.get()) - 1
        
        try:
            tempMinRep = float(self.Entry_FPGA_min_rep.get())
            if tempMinRep > 0:
                self.Entry_FPGA_min_rep.delete(0, END)
                self.Entry_FPGA_min_rep.insert(0, tempMinRep)
            else:
                error = True
                self.Entry_FPGA_min_rep.delete(0, END)
                self.Entry_FPGA_min_rep.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['MIN_TRIGGER_TIME'].value)
                print('Minimum repreat time must be greater than 0')
        except ValueError:
            error = True
            self.Entry_FPGA_min_rep.delete(0, END)
            self.Entry_FPGA_min_rep.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['MIN_TRIGGER_TIME'].value)
            print('Minimum repreat time must be greater than 0')            
        
        try:
            tempCamMinRep = float(self.Entry_FPGA_cam_min_rep.get())
            if tempCamMinRep > 0:
                self.Entry_FPGA_cam_min_rep.delete(0, END)
                self.Entry_FPGA_cam_min_rep.insert(0, tempCamMinRep)
            else:
                error = True
                self.Entry_FPGA_cam_min_rep.delete(0, END)
                self.Entry_FPGA_cam_min_rep.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['CAM_MIN_TRIGGER_TIME'].value)
                print('Minimum repreat time must be greater than 0')
        except ValueError:
            error = True
            self.Entry_FPGA_cam_min_rep.delete(0, END)
            self.Entry_FPGA_cam_min_rep.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['CAM_MIN_TRIGGER_TIME'].value)
            print('Minimum repreat time must be greater than 0')  
        
        try:
            tempFPGAheatpulse = float(self.Entry_heater_pulse.get())
            if tempFPGAheatpulse > 0.1 and tempFPGAheatpulse < 100:
                self.Entry_heater_pulse.delete(0, END)
                self.Entry_heater_pulse.insert(0, '%.1f' % tempFPGAheatpulse)
            else:
                error = True
                self.Entry_heater_pulse.delete(0, END)
                self.Entry_heater_pulse.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['HEATER_PULSE'].value)
                print('Heater pulse needs to be between 0.1 and 100 us')
        except ValueError:
            error = True
            self.Entry_heater_pulse.delete(0, END)
            self.Entry_heater_pulse.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['HEATER_PULSE'].value)
            print('Heater pulse needs to be between 0.1 and 100 us')            
            
        try:
            tempFPGAheatdelay = float(self.Entry_heater_delay.get())
            if tempFPGAheatdelay >= 1 and tempFPGAheatdelay <=1000:
                self.Entry_heater_delay.delete(0, END)
                self.Entry_heater_delay.insert(0, '%.1f' % tempFPGAheatdelay)
            else:
                error = True
                self.Entry_heater_delay.delete(0, END)
                self.Entry_heater_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['HEATER_DELAY'].value)
                print('Heater delay needs to be between 0 and 1000 us')
        except ValueError:
            error = True
            self.Entry_heater_delay.delete(0, END)
            self.Entry_heater_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['HEATER_DELAY'].value)
            print('Heater delay needs to be between 0 and 1000 us')
        
        try:
            tempcamdelay = float(self.Entry_cam_delay.get())
            if tempcamdelay >= 1 and tempcamdelay <= 1000:
                self.Entry_cam_delay.delete(0, END)
                self.Entry_cam_delay.insert(0, '%.1f' % tempcamdelay)
            else:
                error = True
                self.Entry_cam_delay.delete(0, END)
                self.Entry_cam_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['CAM_DELAY'].value)
                print('Camera delay needs to be between 0 and 1000 us')
        except ValueError:
            error = True
            self.Entry_cam_delay.delete(0, END)
            self.Entry_cam_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['CAM_DELAY'].value)
            print('Camera delay needs to be between 0 and 1000 us')
        
        try:
            tempnumstrobe = int(float(self.Entry_strobe_num.get()))
            if tempnumstrobe > -1:
                self.Entry_strobe_num.delete(0, END)
                self.Entry_strobe_num.insert(0, str(tempnumstrobe))
            else:
                error = True
                self.Entry_strobe_num.delete(0, END)
                self.Entry_strobe_num.insert(0, str(self.settings.FPGAsets[var].settings['STROBE_NUM'].value))
                print('Number of strobes needs to be greater or equalt to 0')
        except ValueError:
            error = True
            self.Entry_strobe_num.delete(0, END)
            self.Entry_strobe_num.insert(0, str(self.settings.FPGAsets[var].settings['STROBE_NUM'].value))
            print('Number of strobes needs to be greater or equalt to 0')               
        
        try:
            tempstrobewidth = float(self.Entry_strobe_width.get())
            if tempstrobewidth >= 0:
                self.Entry_strobe_width.delete(0, END)
                self.Entry_strobe_width.insert(0, str(tempstrobewidth))
            else:
                error = True
                self.Entry_strobe_width.delete(0, END)
                self.Entry_strobe_width.insert(0, str(self.settings.FPGAsets[var].settings['STROBE_WIDTH'].value))
                print('Strobe pulse width must be greater than 0')
        except ValueError:
            error = True
            self.Entry_strobe_width.delete(0, END)
            self.Entry_strobe_width.insert(0, str(self.settings.FPGAsets[var].settings['STROBE_WIDTH'].value))
            print('Strobe pulse width must be greater than 0')       
        
        try:
            tempstrobedelay = float(self.Entry_strobe_delay.get())
            if tempstrobedelay >= 1 and tempstrobedelay <=1000:
                self.Entry_strobe_delay.delete(0, END)
                self.Entry_strobe_delay.insert(0, '%.1f' % tempstrobedelay)
            else:
                error = True
                self.Entry_strobe_delay.delete(0, END)
                self.Entry_strobe_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['STROBE_DELAY_1'].value)
                print('Strobe delay needs to be between 0 and 1000 us')
        except ValueError:
            error = True
            self.Entry_strobe_delay.delete(0, END)
            self.Entry_strobe_delay.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['STROBE_DELAY_1'].value)
            print('Strobe delay needs to be between 0 and 1000 us')
            
        try:
            tempstrobesep = float(self.Entry_strobe_separation.get())
            if tempstrobesep >= 1:
                self.Entry_strobe_separation.delete(0, END)
                self.Entry_strobe_separation.insert(0, '%.1f' % tempstrobesep)
            else:
                error = True
                self.Entry_strobe_separation.delete(0, END)
                self.Entry_strobe_separation.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['STROBE_DELAY_2'].value)
                print('Strobe seperation should be between 0 and 1000 us')
        except ValueError:
            error = True
            self.Entry_strobe_separation.delete(0, END)
            self.Entry_strobe_separation.insert(0, '%.1f' % self.settings.FPGAsets[var].settings['STROBE_DELAY_2'].value)
            print('Strobe seperation should be between 0 and 1000 us')                

        try:
            tempFSthresh = float(self.Entry_FS_Threshold.get())
            if tempFSthresh >= 1:
                self.Entry_FS_Threshold.delete(0, END)
                self.Entry_FS_Threshold.insert(0, str(tempFSthresh))
            else:
                error = True
                self.Entry_FS_Threshold.delete(0, END)
                self.Entry_FS_Threshold.insert(0, str(self.settings.FPGAsets[var].settings['FS_THRESHOLD'].value))
                print('FS Threshold must be greater than 0')
        except ValueError:
            error = True
            self.Entry_FS_Threshold.delete(0, END)
            self.Entry_FS_Threshold.insert(0, str(self.settings.FPGAsets[var].settings['FS_THRESHOLD'].value))
            print('FS Threshold must be greater than 0')

        try:
            tempFSgain = float(self.Entry_FS_gain.get())
            if tempFSgain >= 0:
                self.Entry_FS_gain.delete(0, END)
                self.Entry_FS_gain.insert(0, str(tempFSgain))
            else:
                error = True
                self.Entry_FS_gain.delete(0, END)
                self.Entry_FS_gain.insert(0, str(self.settings.FPGAsets[var].settings['FS_PGA_GAIN'].value))
                print('FS Gain must be greater than 0')
        except ValueError:
            error = True
            self.Entry_FS_gain.delete(0, END)
            self.Entry_FS_gain.insert(0, str(self.settings.FPGAsets[var].settings['FS_PGA_GAIN'].value))
            print('FS Gain must be greater than 0')
        
        try:
            tempBSgain = float(self.Entry_BS_gain.get())
            if tempBSgain >= 0:
                self.Entry_BS_gain.delete(0, END)
                self.Entry_BS_gain.insert(0, str(tempBSgain))
            else:
                error = True
                self.Entry_BS_gain.delete(0, END)
                self.Entry_BS_gain.insert(0, str(self.settings.FPGAsets[var].settings['BS_PGA_GAIN'].value))
                print('BS Gain must be greater than 0')
        except ValueError:
            error = True
            self.Entry_BS_gain.delete(0, END)
            self.Entry_BS_gain.insert(0, str(self.settings.FPGAsets[var].settings['BS_PGA_GAIN'].value))
            print('BS Gain must be greater than 0')
            
        try:
            tempFLgain = float(self.Entry_FL_gain.get())
            if tempFLgain >= 0:
                self.Entry_FL_gain.delete(0, END)
                self.Entry_FL_gain.insert(0, str(tempFLgain))
            else:
                error = True
                self.Entry_FL_gain.delete(0, END)
                self.Entry_FL_gain.insert(0, str(self.settings.FPGAsets[var].settings['FL_PGA_GAIN'].value))
                print('FL Gain must be greater than 0')
        except ValueError:
            error = True
            self.Entry_FL_gain.delete(0, END)
            self.Entry_FL_gain.insert(0, str(self.settings.FPGAsets[var].settings['FL_PGA_GAIN'].value))
            print('FL Gain must be greater than 0')
        
        if error == True:
            print("error")
            
        if error == False:
            self.settings.general['CAMERA_NUMBER'].value = temp
            self.settings.general['CAMX'].value = tempx
            self.settings.general['CAMY'].value = tempy
            self.settings.detection['MAX_THRESH'].value = tempmaxthresh
            self.settings.detection['MIN_THRESH'].value = tempminthresh
            self.settings.detection['MIN_AREA'].value = tempminbead
            self.settings.detection['MAX_AREA'].value = tempmaxbead
            self.settings.detection['BEAD_CIRC'].value = tempbeadcirc
            self.settings.general['FPGA_NUMBER'].value = tempFPGAnum
            
            for i in np.arange(0, self.settings.general['FPGA_NUMBER'].value):
                self.settings.FPGAsets[i].settings['COMPORT'].value = tempFPGAport
                
            if self.CheckBox_FPGA_set_all_var.get():
                krange = np.arange(0, self.settings.general['FPGA_NUMBER'].value)
            else:
                krange = np.arange(var, var+1)
            
            mode = self.settings.FPGAsets[var].settings['FPGA_MODE'].value
            for k in krange:
                self.settings.FPGAsets[k].settings['MIN_TRIGGER_TIME'].value = tempMinRep
                self.settings.FPGAsets[k].settings['CAM_MIN_TRIGGER_TIME'].value = tempCamMinRep
                self.settings.FPGAsets[k].settings['HEATER_PULSE'].value = tempFPGAheatpulse
                self.settings.FPGAsets[k].settings['HEATER_DELAY'].value = tempFPGAheatdelay
                self.settings.FPGAsets[k].settings['CAM_DELAY'].value = tempcamdelay
                self.settings.FPGAsets[k].settings['STROBE_NUM'].value = tempnumstrobe
                self.settings.FPGAsets[k].settings['STROBE_WIDTH'].value = tempstrobewidth
                self.settings.FPGAsets[k].settings['STROBE_DELAY_1'].value = tempstrobedelay                
                self.settings.FPGAsets[k].settings['STROBE_DELAY_2'].value = tempstrobesep
                self.settings.FPGAsets[k].settings['FS_THRESHOLD'].value = tempFSthresh
                self.settings.FPGAsets[k].settings['FS_PGA_GAIN'].value = tempFSgain
                self.settings.FPGAsets[k].settings['BS_PGA_GAIN'].value = tempBSgain
                self.settings.FPGAsets[k].settings['FL_PGA_GAIN'].value = tempFLgain

                if mode == 1:
                    self.settings.FPGAsets[k].settings['FPGA_MODE'].value = 1
                elif mode == 2:
                    self.settings.FPGAsets[k].settings['FPGA_MODE'].value = 2
                else:
                    self.settings.FPGAsets[k].settings['FPGA_MODE'].value = 0
            self.CheckBox_FPGA_set_all_var.set(False)    
            self.settings.general['UPDATE_SETTINGS'].value = True
           
        
    def send(self):
        print("settings set")
        
        self.top.destroy()
    
    def Exit(self):
        self.top.destroy()