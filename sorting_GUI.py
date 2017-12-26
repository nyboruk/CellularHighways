# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:28:51 2017

@author: Robyn.Pritchard
"""


import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image
import cv2
import image_processing_functions2 as ip
from settingsGUI import SettingsPopUp
from SettingsClasses import *
import imutils as imu
from copy import copy, deepcopy
import FPGA_control_modbus_tk as FPGA
import numpy as np
from FPGA_GUI import FpgaPopUp
from ValidPopUp import ValidPopUp        
class mainWindow:
    
    def __init__(self, master, *args, **kwargs):
        
#        tk.Tk.__init__(self, *args, **kwargs)        

        self.settings = settings()
        self.settings = self.settings.load_configs()
        self.detector = ip.detector_setup(self.settings)
        self.myFPGAs = 0
        self.master = master
        self.master.iconbitmap(self, default = "highwaysicon.ico")
        self.master.resizable(0,0)
        self.master.protocol("WM_DELETE_WINDOW", self.Exit)
        
        self.imageFrame = tk.Frame(self.master, width = 1000, height = 700)
        self.imageFrame.grid(row  = 0, column = 0, padx = 5, pady = 5)
        self.imageFrame = Label(self.imageFrame)
        self.imageFrame.grid(row = 20, column = 20)
        
        ###Menus
        self.menu = Menu(self.master)
        self.master.config(menu = self.menu, background = "#FFFFFF")
                           
        self.subMenu = Menu(self.menu)
        self.menu.add_cascade(label = "File", menu = self.subMenu)
        self.subMenu.add_command(label = "Load Video", command = self.LoadVideo)  
        self.subMenu.add_command(label = "Open Camera", command = self.OpenCamera)
        self.subMenu.add_command(label = "Settings", command = self.SettingsDialog)
        self.subMenu.add_command(label = "Exit", command = self.Exit)
        
        self.Playback = Menu(self.menu)
        self.menu.add_cascade(label = "Playback", menu = self.Playback)
        self.Playback.add_command(label = "Pause", command = self.pause)
        self.Playback.add_command(label = "Resume", command = self.resume)
        self.Playback.add_command(label = "Stop", command = self.stop)
        self.Playback.add_command(label = "Start Recording", command = self.StartRecording)
        self.Playback.add_command(label = "Stop Recording", command = self.StopRecording)
        
        self.Automation = Menu(self.menu)
        self.menu.add_cascade(label = "Automation", menu = self.Automation)
        
        self.FPGAmenu = Menu(self.menu)
        self.menu.add_cascade(label = "FPGA", menu = self.FPGAmenu)
        self.FPGAmenu.add_command(label = "Connect", command = self.InitFPGAs)
        self.FPGAmenu.add_command(label = "Controller", command = self.FPGAcont)
        self.FPGAmenu.add_command(label = "Disconnect", command = self.FPGAdisc)
        
        self.dataMenu = Menu(self.menu)
        self.menu.add_cascade(label = "Data", menu = self.dataMenu)
        self.dataMenu.add_command(label = "Save Data", command = self.SaveData)
        self.dataMenu.add_command(label = "Load Data", command = self.LoadData)
        self.dataMenu.add_command(label = "Plot Data", command = self.PlotData)
        self.dataMenu.add_command(label = "Plot SortWindow", command = self.PlotSortWindow)
        
        
        ###Control Frame
        self.controls = LabelFrame(self.imageFrame, text = 'Controls', font = "Consolas 11 bold")
        self.controls.grid(row = 0, column = 0, rowspan = 10, ipadx = 5, ipady = 5, sticky = 'news')
        self.blankspace = Label(self.controls)
        self.blankspace.grid(row = 0, column = 0, sticky = 'we')
        
        '''Detection Controls'''
       
        ### Title
        self.detConts = LabelFrame(self.controls, text = "Detection Parameters", font = "Consolas 10 bold")
        self.detConts.grid(row = 1, column = 0, sticky = 'nesw', ipadx = 5, ipady = 5, columnspan = 1)
        
        ### Minimum Threshold Slider
        Label(self.detConts, text = "Lower Thresh", font = "Consolas 10").grid(row = 0, column = 1, sticky = 'ws')
        self.MinThreshScaler = Scale(self.detConts, from_ = 0, to = 255, resolution = 1, orient = HORIZONTAL, length = 200, command = self.scalebars)
        self.MinThreshScaler.grid(row = 0, column = 0, columnspan = 1, sticky = 'news')
        
        ### Maximum Threshold Slider
        Label(self.detConts, text = "Upper Thresh", font = "Consolas 10").grid(row = 1, column = 1, sticky = 'ws')
        self.MaxThreshScaler = Scale(self.detConts, from_ = 0, to = 255, resolution = 1, orient = HORIZONTAL, length = 200, command = self.scalebars)
        self.MaxThreshScaler.grid(row = 1, column = 0, columnspan = 1, sticky = 'news')
        
        ### Minimum bead area slider
        Label(self.detConts, text = "Min Bead size", font = "Consolas 10").grid(row = 2, column = 1, sticky = 'ws')
        self.MinBeadScaler = Scale(self.detConts, from_ = 10, to = 100, resolution = 1, orient = HORIZONTAL, length = 200, command = self.scalebars)
        self.MinBeadScaler.grid(row = 2, column = 0, columnspan = 1, sticky = 'news')
        
        ### Maximum bead area slider
        Label(self.detConts, text = "Max Bead size", font = "Consolas 10").grid(row = 3, column = 1, sticky = 'ws')
        self.MaxBeadScaler = Scale(self.detConts, from_ = 20, to = 200, resolution = 1, orient = HORIZONTAL, length = 200, command = self.scalebars)
        self.MaxBeadScaler.grid(row = 3, column = 0, columnspan = 1, sticky = 'news')

        ### toggle fill holes analysis
        self.toggle_fill_holes_btn = tk.Button(self.detConts, text = "Fill holes ON/OFF", width = 5, command = self.thresh_fill_toggle)
        self.toggle_fill_holes_btn.grid(row = 4, column = 0, columnspan = 2, sticky = 'nesw', padx = 10, pady = 10)
        
        ### toggle display images
        self.toggle_disp_btn = tk.Button(self.detConts, text = "Analyis Image ON/OFF", width = 5, command = self.disp_toggle)
        self.toggle_disp_btn.grid(row = 5, column = 0, columnspan = 2, sticky = 'nesw', padx = 10, pady = 10)
        
        ### toggle full window mode
        self.toggle_full_window_btn = tk.Button(self.detConts, text = "Full Window ON/OFF", width = 5, command = self.window_toggle)
        self.toggle_full_window_btn.grid(row = 6, column = 0, columnspan = 2, sticky = 'news', padx = 10, pady = 10)
        

        self.set_settings()
        self.VideoFrameCreate()
        
        ### start loops
        self.house_keeping()


    def VideoFrameCreate(self):
        ### Video Frame

        self.VideoFrame = LabelFrame(self.imageFrame, width = self.settings.detection['ROI'].value[2], height = self.settings.detection['ROI'].value[3])
        self.VideoFrame.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan = 2)
        self.imagePreviewFrame = tk.Frame(self.VideoFrame, width = self.settings.detection['ROI'].value[2], height = self.settings.detection['ROI'].value[3])
        self.imagePreviewFrame.grid(padx = 5, pady = 5, sticky = 'nesw')
        self.imagePreviewFrame.grid_propagate(0)
        self.display1 = tk.Label(self.imagePreviewFrame)
        self.display1.grid(row = 0, column = 0, sticky = 'nesw')
        self.display1.place(in_ = self.imagePreviewFrame, anchor = "c", relx = .5, rely = .5)
        
    def set_settings(self):
        '''This function sets all the GUI items to values in the settings.
        It will disable GUI objects depending on those settings'''
        
        ### set scale bars to values in settings
        self.MaxThreshScaler.set(self.settings.detection['MAX_THRESH'].value)
        self.MinThreshScaler.set(self.settings.detection['MIN_THRESH'].value)
        self.MaxBeadScaler.set(self.settings.detection['MAX_AREA'].value)
        self.MinBeadScaler.set(self.settings.detection['MIN_AREA'].value)
        
        ### set buttos to On/Off states
        if self.settings.general['FILL_HOLES'].value:
            self.toggle_fill_holes_btn.config(relief = "sunken", background = 'pale green')
        else:
            self.toggle_fill_holes_btn.config(relief = "raised", background = 'tomato' )
            
        if self.settings.general['SUB_BACKGROUND'].value:
            self.toggle_disp_btn.config(relief = "sunken", background = 'pale green')
        else:
            self.toggle_disp_btn.config(relief = "raised", background = 'tomato' )
            
        if self.settings.general['FULL_WINDOW'].value:
            self.toggle_full_window_btn.config(relief = "sunken", background = 'pale green')
        else:
            self.toggle_full_window_btn.config(relief = "raised", background = 'tomato' )
        
        ### disable relevant menus
        if self.settings.general['ITEM_LOADED'].value == False:
            self.Playback.entryconfig("Resume", state = 'disabled')
            self.Playback.entryconfig("Stop", state = 'disabled')
            self.Playback.entryconfig("Pause", state = 'disabled')
            self.Playback.entryconfig("Start Recording", state = 'disabled')
            self.Playback.entryconfig("Stop Recording", state = 'disabled')
        if self.settings.general['FPGA_CONNECTED'].value == False:
            self.FPGAmenu.entryconfig("Controller", state = 'disabled')
            self.FPGAmenu.entryconfig("Disconnect", state = 'disabled')
            
    def SettingsDialog(self):
        self.w = SettingsPopUp(self.master, self.settings)
        self.master.wait_window(self.w.top)
        
    def house_keeping(self):
        if self.settings.general['RUNNING'].value == False:
            if self.settings.general['UPDATE_SETTINGS'].value:
                self.update()
        self.master.after(200, self.house_keeping)
    
    def OpenCamera(self):
        self.settings.general['LOAD_VIDEO'].value = False
        self.StartVideo()
    
    def LoadVideo(self):
        self.settings.general['LOAD_VIDEO'].value = True
        self.StartVideo()    
                
    def Exit(self):
        if self.settings.general['RECORD'].value:
            self.StopRecording()
        if self.settings.general['FULL_WINDOW'].value == True:
            cv2.destroyWindow('Full Window')
        if self.settings.general['FPGA_CONNECTED'].value == True:
            self.FPGAdisc()
            
        self.settings.save_configs()
        self.master.destroy()
        self.master.quit()
      
    def pause(self):
        self.settings.general['RUNNING'].value = False
        self.Menuconfig()
        
    def resume(self):
        self.settings.general['RUNNING'].value = True
        self.Menuconfig()
        self.VideoCapture()

    
    def stop(self):
        self.settings.general['RUNNING'].value = False
        if self.settings.general['RECORD'].value:
            self.StopRecording()
        self.vs.stop()
        self.settings.general['ITEM_LOADED'].value = False
        self.Menuconfig()
        self.Playback.entryconfig('Stop Recording', state = 'disabled')
        self.Playback.entryconfig('Start Recording', state = 'disabled')
        
    def update(self):
        self.settings.general['UPDATE_SETTINGS'].value = False
        self.detector.clear()
        self.detector = ip.detector_setup(self.settings)
        self.set_settings()
        if self.settings.general['FPGA_CONNECTED'].value == True:
            for i in np.arange(0, self.settings.general['FPGA_NUMBER'].value):
                print("writing to FPGA: " + str(self.settings.general['FPGA_NUMBER'].value+1))
                self.myFPGAs[i].write_to_FPGA()
        
    def disp_toggle(self):    
        if self.settings.general['SUB_BACKGROUND'].value:
            self.settings.general['SUB_BACKGROUND'].value = False
            self.toggle_disp_btn.config(relief = "raised", background = 'tomato')
        else:
            self.settings.general['SUB_BACKGROUND'].value = True
            self.toggle_disp_btn.config(relief = "sunken", background = 'pale green')
    
    def thresh_fill_toggle(self):    
        if self.settings.general['FILL_HOLES'].value:
            self.settings.general['FILL_HOLES'].value = False
            self.toggle_fill_holes_btn.config(relief = "raised", background = 'tomato')
        else:
            self.settings.general['FILL_HOLES'].value = True
            self.toggle_fill_holes_btn.config(relief = "sunken", background = 'pale green')
    
    def window_toggle(self):
        if self.settings.general['FULL_WINDOW'].value:
            self.VideoFrameCreate()
            self.settings.general['FULL_WINDOW'].value = False
            self.toggle_full_window_btn.config(relief = "raised", background = 'tomato')
            cv2.destroyWindow('Full Window')

        else:
            self.settings.general['FULL_WINDOW'].value = True
            self.toggle_full_window_btn.config(relief = "sunken", background = 'pale green')
            self.VideoFrame.grid_forget()
            cv2.namedWindow('Full Window', cv2.WINDOW_GUI_EXPANDED)
            
    def scalebars(self, val):
        self.settings.detection['MIN_AREA'].value = int(self.MinBeadScaler.get())
        self.settings.detection['MAX_AREA'].value = int(self.MaxBeadScaler.get())
        self.settings.detection['MAX_THRESH'].value = int(self.MaxThreshScaler.get())
        self.settings.detection['MIN_THRESH'].value = int(self.MinThreshScaler.get())
        self.detector.clear()
        self.detector = ip.detector_setup(self.settings)
    
    def StartVideo(self):
        
        ### if a video is loaded release it
        if self.settings.general['RUNNING'].value:
            self.stop()
        
        ### open video
        self.vs = ip.open_footage(self.settings)
        frame = self.vs.read()
        
        if not self.vs.stopped:
            ### set footage as loaded
            self.settings.general['ITEM_LOADED'].value = True
            [self.settings, self.avg, self.mask_waste, self.mask_sort] = ip.initialise(frame, self.settings)
            
            
            if self.settings.general['DETECTION_ON'].value:
                self.beads = ip.bead_data()
                self.counts = counts()
                self.detector = ip.detector_setup(self.settings)
            
            ###set frame size to that of the footage
            self.imagePreviewFrame.config(width = self.settings.detection['ROI'].value[2], height = self.settings.detection['ROI'].value[3])
            
            ### if recording is on from the start, begin recording routine
            if self.settings.general['RECORD'].value:
                self.StartRecording()
            
            ### set to state to running
            self.settings.general['RUNNING'].value = True
            
            ###disabled/enabled menus
            self.Playback.entryconfig('Start Recording', state = 'normal')
            self.Menuconfig()
            
            ### start video capture loop
            self.vs.resume()
            self.VideoCapture()
        else:
            print("couldn't load video")
            
    def VideoCapture(self):
        if self.vs.more():
            frame = self.vs.read()
            
            if self.settings.general['UPDATE_SETTINGS'].value:
                self.update()
                
            if not self.vs.stopped:
                if self.settings.general['RECORD_RAW'].value == True and self.settings.general['RECORD'].value == True:
                    self.record.write(frame)
                    
                frame, original, self.avg, self.detector = ip.detection_setup(frame, self.avg, self.detector, self.settings, self.mask_waste, self.mask_sort)
                if self.settings.general['DETECTION_ON'].value:
                    count = -1
                    disp, self.counts, self.beads, count = ip.find_beads(frame, original, self.detector, self.settings, self.counts, self.beads)
                    disp = ip.draw_info(disp, self.counts, self.settings)
                else: disp = frame
                
                if self.settings.general['RECORD'].value == True and self.settings.general['RECORD_RAW'].value == False:
                    self.record.write(disp)
                    xc = int(20)
                    yc = self.settings.detection['ROI'].value[3]-int(20)
                    cv2.putText(disp, 'REC', (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255))
                    cv2.circle(disp, (xc+48, yc-6), int(7), (0,0,255), -1)
                
                if self.settings.general['RECORD_RAW'].value == True and self.settings.general['RECORD'].value == True:
                    xc = int(20)
                    yc = self.settings.detection['ROI'].value[3] - int(20)
                    cv2.putText(disp, 'RAW REC', (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255))
                    cv2.circle(disp, (xc+96, yc-6), int(7), (0,0,255), -1)
                    
                if self.settings.general['FULL_WINDOW'].value:
                    cv2.imshow('Full Window', disp)
                else:
                    #TkInter process for displaying the video
                    color = cv2.cvtColor(disp, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(color)
                    imgtk = ImageTk.PhotoImage(image = img)
                    self.display1.imgtk = imgtk
                    self.display1.configure(image = imgtk)
                    
            if self.settings.general['VALIDATION_ON'].value:
                if count > -1:
                    if self.beads.data[count, 8] == -1:
                        vp = ValidPopUp(self.master)
                        if vp.result == True:
                            self.beads.data[count,8:10] = [0,0]
                            print("undetected bead")
                    
        if self.settings.general['RUNNING'].value:
            self.master.after(5, self.VideoCapture)

    def StartRecording(self):
  
        video_path = filedialog.asksaveasfilename()
        video_path_analysed = video_path + '.avi'
        
        if self.settings.general['RECORD_RAW'].value:
            fourcc = cv2.VideoWriter_fourcc(*'FFV1')
            frame_size = self.settings.general['FRAME_SIZE_RAW'].value
        else:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_size = self.settings.general['FRAME_SIZE'].value
            print("Frame size is :")
            print(self.settings.general['FRAME_SIZE'].value)

        
        self.record = cv2.VideoWriter(video_path_analysed,fourcc = fourcc, fps=20.0, frameSize=frame_size)

        self.settings.general['RECORD'].value = True
        self.Playback.entryconfig("Stop Recording", state = 'normal')
        self.Playback.entryconfig("Start Recording", state = 'disabled')
    
    def StopRecording(self):
        self.settings.general['RECORD'].value = False
        self.record.release()
        self.Playback.entryconfig("Start Recording", state = 'normal')
        self.Playback.entryconfig("Stop Recording", state = 'disabled')

    def Menuconfig(self):
        if self.settings.general['ITEM_LOADED'].value == True and self.settings.general['RUNNING'].value == True:
            self.Playback.entryconfig("Resume", state = 'disabled')
            self.Playback.entryconfig("Stop", state = 'normal')
            self.Playback.entryconfig("Pause", state = 'normal')
        elif self.settings.general['ITEM_LOADED'].value == True and self.settings.general['RUNNING'].value == False:
            self.Playback.entryconfig("Resume", state = 'normal')
            self.Playback.entryconfig("Stop", state = 'normal')
            self.Playback.entryconfig("Pause", state = 'disabled')       
        elif self.settings.general['ITEM_LOADED'].value == False:
            self.Playback.entryconfig("Resume", state = 'disabled')
            self.Playback.entryconfig("Stop", state = 'disabled')
            self.Playback.entryconfig("Pause", state = 'disabled')
    
    def InitFPGAs(self):
        self.myFPGAs = np.ndarray((self.settings.general['FPGA_NUMBER'].value), dtype = object)
        try:
            for i in np.arange(0, self.settings.general['FPGA_NUMBER'].value):
                self.myFPGAs[i] = FPGA.FPGA(self.settings.FPGAsets[i])
                self.myFPGAs[i].write_to_FPGA(True)
            self.settings.general['FPGA_CONNECTED'].value = True
            self.FPGAmenu.entryconfig("Controller", state = 'normal')
            self.FPGAmenu.entryconfig("Disconnect", state = 'normal')
            self.FPGAmenu.entryconfig("Connect", state = 'disable')
        except:
            print("Couldn't connect to FPGAs")
            
    def FPGAcont(self):
        print("Open FPGA controller")
        self.f = FpgaPopUp(self.master, self.settings, self.myFPGAs)
        self.master.wait_window(self.f.top)
        
    def FPGAdisc(self):
        for i in np.arange(0, self.settings.general['FPGA_NUMBER'].value):
            self.myFPGAs[i].disconnect()
        self.settings.general['FPGA_CONNECTED'].value = False
        print("FPGAs disconnected")
        self.FPGAmenu.entryconfig("Controller", state = 'disable')
        self.FPGAmenu.entryconfig("Disconnect", state = 'disable')
        self.FPGAmenu.entryconfig("Connect", state = 'normal')
    
    def SaveData(self):
        self.beads.save()
        
    def LoadData(self):
        self.beads = ip.bead_data()
        self.beads.load()
        
    def PlotData(self):
        self.beads.find_valid()
        self.beads.plot_separated_beads()
    
    def PlotSortWindow(self):
        self.beads.find_sort_window()

            

     
root = tk.Tk()
root.wm_title("Cellular Highways at TTP PLC")
m = mainWindow(root)

root.mainloop()