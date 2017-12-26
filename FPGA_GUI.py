# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:10:41 2017

@author: Robyn.Pritchard
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
import image_processing_functions as ip
import numpy as np
from SettingsClasses import *

class FpgaPopUp:
    def __init__(self, parent, settings, myFPGAs = 0):
        self.writeFPGA = True
        self.myFPGAs = myFPGAs
        self.Sweeping = False
        self.settings = settings
        self.currentFPGA = self.settings.general['CURRENT_FPGA'].value
        self.led1delay = self.settings.FPGAsets[self.currentFPGA-1].settings['STROBE_DELAY_1'].value
        self.led2delay = self.settings.FPGAsets[self.currentFPGA-1].settings['STROBE_DELAY_2'].value
        self.heatdelay = self.settings.FPGAsets[self.currentFPGA-1].settings['HEATER_DELAY'].value
        self.mastershift = 0.0
        top = self.top = tk.Toplevel(parent)
        self.top.resizable(0,0)
        self.top.protocol("WM_DELETE_WINDOW", self.Exit)
        
        self.MainFrame = tk.Frame(self.top, width = 400, height = 400)
        self.MainFrame.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        self.FPGAFrame = LabelFrame(self.MainFrame, text = 'FPGA Controller', font = "Consolas 12 bold")
        self.FPGAFrame.grid(row = 0, column = 0, ipadx = 5, ipady = 5, sticky = 'news')

        self.mainbarFrame = LabelFrame(self.FPGAFrame, text = "Individual Control", font = "Consolas 10 bold")
        self.mainbarFrame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = 5, ipadx = 5, ipady = 5)

        rownum = 0
        entwidth = 5
        self.Entryled1min = Entry(self.mainbarFrame, width = entwidth)
        self.Entryled1min.grid(row = rownum, column = 0, sticky = 's')
        self.led1scaler = Scale(self.mainbarFrame, from_ = 0, to = 1000, resolution = 0.1, orient = HORIZONTAL, length = 200, command = self.led1bar)
        self.led1scaler.grid(row = rownum, column = 1, columnspan = 1, sticky = 's')
        self.Entryled1max = Entry(self.mainbarFrame, width = entwidth)
        self.Entryled1max.grid(row = rownum, column = 2, sticky = 's')
        rownum += 1
        
        Label(self.mainbarFrame, text = "min", font = "Consolas 8").grid(row = rownum, column = 0, sticky = 'news')
        Label(self.mainbarFrame, text = "LED1 DELAY", font = "Consolas 10").grid(row = rownum, column = 1, sticky = 'news')
        Label(self.mainbarFrame, text = "max", font = "Consolas 10").grid(row = rownum, column = 2, sticky = 'news')
        rownum += 1
        
        self.Entryled2min = Entry(self.mainbarFrame, width = entwidth)
        self.Entryled2min.grid(row = rownum, column = 0, sticky = 's')
        self.led2scaler = Scale(self.mainbarFrame, from_ = 0, to = 1000, resolution = 0.1, orient = HORIZONTAL, length = 200, command = self.led2bar)
        self.led2scaler.grid(row = rownum, column = 1, columnspan = 1, sticky = 'news')
        self.Entryled2max = Entry(self.mainbarFrame, width = entwidth)
        self.Entryled2max.grid(row = rownum, column = 2, sticky = 's')
        rownum += 1
        
        Label(self.mainbarFrame, text = "min", font = "Consolas 8").grid(row = rownum, column = 0, sticky = 'news')
        Label(self.mainbarFrame, text = "LED2 DELAY", font = "Consolas 10").grid(row = rownum, column = 1, sticky = 'news')
        Label(self.mainbarFrame, text = "max", font = "Consolas 10").grid(row = rownum, column = 2, sticky = 'news')
        rownum += 1  
        
        self.Entryheatermin = Entry(self.mainbarFrame, width = entwidth)
        self.Entryheatermin.grid(row = rownum, column = 0, sticky = 's')
        self.heaterscaler = Scale(self.mainbarFrame, from_ = 0, to = 1000, resolution = 0.1, orient = HORIZONTAL, length = 200, command = self.heaterbar)
        self.heaterscaler.grid(row = rownum, column = 1, columnspan = 1, sticky = 'news')
        self.Entryheatermax = Entry(self.mainbarFrame, width = entwidth)
        self.Entryheatermax.grid(row = rownum, column = 2, sticky = 's')
        rownum += 1
        
        Label(self.mainbarFrame, text = "min", font = "Consolas 8").grid(row = rownum, column = 0, sticky = 'news')
        Label(self.mainbarFrame, text = "HEATER DELAY", font = "Consolas 10").grid(row = rownum, column = 1, sticky = 'news')
        Label(self.mainbarFrame, text = "max", font = "Consolas 10").grid(row = rownum, column = 2, sticky = 'news')
        rownum += 1
        
        self.masterbarFrame = LabelFrame(self.FPGAFrame, text = "Master Control", font = "Consolas 10 bold")
        self.masterbarFrame.grid(row = 2, column = 0, padx = 5, pady = 5, ipadx = 5, ipady = 5)
        
        self.Entrymastermin = Entry(self.masterbarFrame, width = entwidth)
        self.Entrymastermin.grid(row = 0, column = 0, sticky = 's')
        self.masterscaler = Scale(self.masterbarFrame, from_ = -50, to = 50, resolution = 0.1, orient = HORIZONTAL, length = 200, command = self.masterbar)
        self.masterscaler.grid(row = 0, column = 1, columnspan = 1, sticky = 'news')
        self.Entrymastermax = Entry(self.masterbarFrame, width = entwidth)
        self.Entrymastermax.grid(row = 0, column = 2, sticky = 's')

        Label(self.masterbarFrame, text = "min", font = "Consolas 8").grid(row = 1, column = 0, sticky = 'news')
        Label(self.masterbarFrame, text = "MASTER SHIFT", font = "Consolas 10").grid(row = 1, column = 1, sticky = 'news')
        Label(self.masterbarFrame, text = "max", font = "Consolas 10").grid(row = 1, column = 2, sticky = 'news')        
        self.ButtonRange = Button(self.FPGAFrame, text = "Set Ranges", background = "ivory", command = self.rangechange)

        self.ButtonRange.grid(row = 3, column = 0, sticky = 'ns')

        self.sweepFrame = LabelFrame(self.FPGAFrame, text = "Sweep Control", font = "Consolas 10 bold")
        self.sweepFrame.grid(row = 0, column = 1, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = 'news')
        
        Label_sweep = Label(self.sweepFrame, text = "Bar to sweep: ").grid(row = 0, column = 0, sticky = 'e')
        self.SweepID = StringVar()
        SweepIDs = ['Master', 'LED1', 'LED2', 'Heater']
        self.SweepID.set('Master')
        self.SweepIDMenu = OptionMenu(self.sweepFrame, self.SweepID, *SweepIDs)
        self.SweepIDMenu.grid(row = 0, column = 1, sticky = 'ew')
        
        Label(self.sweepFrame, text = "Sweep time [s]: ").grid(row = 1, column = 0, sticky = 'e')
        self.EntrySweeptime = Entry(self.sweepFrame, width = 13)
        self.EntrySweeptime.grid(row = 1, column = 1)
        Label(self.sweepFrame, text = "Step size [us]: ").grid(row = 2, column = 0, sticky = 'e')
        self.EntrySweepStep = Entry(self.sweepFrame, width = 13)
        self.EntrySweepStep.grid(row = 2, column = 1)
        self.ButtonStartSweep = Button(self.sweepFrame, text = "Start Sweep", bg = 'ivory', command = self.StartSweep)
        self.ButtonStartSweep.grid(row = 4, column = 0, columnspan = 2, sticky = 'ew', padx = 15, pady = 5)
        self.ButtonStopSweep = Button(self.sweepFrame, text = "Stop Sweep", bg = 'tomato', command = self.StopSweep)
        self.ButtonStopSweep.grid(row = 5, column = 0, columnspan = 2, sticky = 'ew', padx = 15, pady = 5)
        self.setvalues()
        
    def setvalues(self):
        
        self.led1scaler.set(self.led1delay)
        self.led2scaler.set(self.led2delay)
        self.heaterscaler.set(self.heatdelay)
        
        self.Entryled1min.delete(0,END)
        self.Entryled1min.insert(0, '%.1f' % (1.0))
        self.Entryled1max.delete(0, END)
        self.Entryled1max.insert(0, '%.1f' % (self.led1delay + 100))
        self.led1scaler.config(from_ = 1, to = self.led1delay+100)
        
        self.Entryled2min.delete(0, END)
        self.Entryled2min.insert(0,'%.1f' % (self.led1delay))
        self.Entryled2max.delete(0, END)
        self.Entryled2max.insert(0, '%.1f' % (self.led2delay+100))
        self.led2scaler.config(from_ = self.led1delay, to = self.led2delay+100)
        
        self.Entryheatermin.delete(0, END)
        self.Entryheatermin.insert(0, str(1.0))
        self.Entryheatermax.delete(0, END)
        self.Entryheatermax.insert(0, '%.1f' % (self.heatdelay+100))
        self.heaterscaler.config(from_ = 1, to = self.heatdelay+100)
        
        self.Entrymastermin.delete(0, END)
        self.Entrymastermin.insert(0, '%.1f' % -50.0)
        self.Entrymastermax.delete(0, END)
        self.Entrymastermax.insert(0, '%.1f' % 50.0)
        
        self.EntrySweeptime.delete(0, END)
        self.EntrySweeptime.insert(0, '%.1f' % 120)
        
        self.EntrySweepStep.delete(0, END)
        self.EntrySweepStep.insert(0, '%.1f' % 1.0)
        
    
    def led1bar(self, val):
        if float(val) != (self.led1delay- self.mastershift):
            self.led1delay = float(val) - self.mastershift
            self.settings.FPGAsets[self.settings.general['CURRENT_FPGA'].value-1].settings['STROBE_DELAY_1'].value = float(val)
            if self.writeFPGA:
                self.myFPGAs[self.settings.general['CURRENT_FPGA'].value - 1].write_to_FPGA()
            print("led1 bar changed to: " + str(val))
    
    def led2bar(self, val):
        if float(val) != (self.led2delay):
            self.led2delay = float(val)
            self.settings.FPGAsets[self.settings.general['CURRENT_FPGA'].value-1].settings['STROBE_DELAY_2'].value = float(val)
            if self.writeFPGA:
                self.myFPGAs[self.settings.general['CURRENT_FPGA'].value-1].write_to_FPGA()
            print("led2 bar changed to: " + str(val))
        
    def heaterbar(self, val):
        if float(val) != (self.heatdelay - self.mastershift):
            self.heaterdelay = float(val) - self.mastershift
            self.settings.FPGAsets[self.settings.general['CURRENT_FPGA'].value-1].settings['HEATER_DELAY'].value = float(val)
            if self.writeFPGA:
                self.myFPGAs[self.settings.general['CURRENT_FPGA'].value-1].write_to_FPGA()
            print("heater bar changed to: " + str(val))
    
    def masterbar(self, val):
        self.mastershift = float(val)
        self.led1scaler.set(self.led1delay + self.mastershift)
        self.heaterscaler.set(self.heatdelay + self.mastershift)
        
    def rangechange(self):
        error = False
        try:
            ld1min = float(self.Entryled1min.get())
            ld1min = float(int(ld1min*10)/10)
            self.Entryled1min.delete(0, END)
            self.Entryled1min.insert(0, '%.1f' % ld1min)
        except ValueError:
            error = True
            print("Invalid input")
        
        try:
            ld1max = float(self.Entryled1max.get())
            ld1max = float(int(ld1max*10)/10)
            self.Entryled1max.delete(0, END)
            self.Entryled1max.insert(0, '%.1f' % ld1max)
        except ValueError:
            error = True
            print("Invalid input")
            
        try:
            ld2min = float(self.Entryled2min.get())
            ld2min = float(int(ld2min*10)/10)
            self.Entryled2min.delete(0, END)
            self.Entryled2min.insert(0, '%.1f' % ld2min)
        except ValueError:
            error = True
            print("Invalid input")
        
        try:
            ld2max = float(self.Entryled2max.get())
            ld2max = float(int(ld2max*10)/10)
            self.Entryled2max.delete(0, END)
            self.Entryled2max.insert(0, '%.1f' % ld2max)
        except ValueError:
            error = True
            print("Invalid input")
            
        try:
            heatmin = float(self.Entryheatermin.get())
            heatmin = float(int(heatmin*10)/10)
            self.Entryheatermin.delete(0, END)
            self.Entryheatermin.insert(0, '%.1f' % heatmin)
        except ValueError:
            error = True
            print("Invalid input")
        
        try:
            heatmax = float(self.Entryheatermax.get())
            heatmax = float(int(heatmax*10)/10)
            self.Entryheatermax.delete(0, END)
            self.Entryheatermax.insert(0, '%.1f' % heatmax)
        except ValueError:
            error = True
            print("Invalid input")
        
        try:
            mastermin = float(self.Entrymastermin.get())
            mastermin = float(int(mastermin*10)/10)
            self.Entrymastermin.delete(0,END)
            self.Entrymastermin.insert(0, '%.1f' % mastermin)
        except ValueError:
            error = True
            print("Invalid input")
            
        try:
            mastermax = float(self.Entrymastermax.get())
            mastermax = float(int(mastermax*10)/10)
            self.Entrymastermax.delete(0, END)
            self.Entrymastermax.insert(0, '%.1f' % mastermax)
        except ValueError:
            error = True
            print("Invalid input")
            
        if error == False:
            self.led1scaler.config(from_ = ld1min, to = ld1max)
            if ld2min < ld1max:
                ld2min = ld1max + 1.0
                self.Entryled2min.delete(0, END)
                self.Entryled2min.insert(0, '%.1f' % ld2min)
            self.led2scaler.config(from_ = ld2min, to = ld2max)
            self.heaterscaler.config(from_ = heatmin, to = heatmax)
            self.masterscaler.config(from_ = mastermin, to = mastermax)
            
    def StartSweep(self):
        self.Sweeping = True
        self.Sweeping_bar = self.SweepID.get()
        self.SweepStepSize = float(self.EntrySweepStep.get())

        if self.SweepID.get() == 'Master':
            self.currentstep = float(self.Entrymastermin.get())
            self.SweepEnd = float(self.Entrymastermax.get())
        elif self.SweepID.get() == 'LED1':
            self.currentstep = float(self.Entryled1min.get())
            self.SweepEnd = float(self.Entryled1max.get())
        elif self.SweepID.get() == 'LED2':
            self.currentstep = float(self.Entryled2min.get())
            self.SweepEnd = float(self.Entryled2max.get())
        elif self.SweepID.get() == 'Heater':
            self.currentstep = float(self.Entryheatermin.get())
            self.SweepEnd = float(self.Entryheatermax.get())
        else:
            self.stepdelay = 0
            self.Sweeping = False
            print("error")
        
        self.stepdelay = self.SweepEnd - self.currentstep    
        self.stepdelay = self.stepdelay/self.SweepStepSize
        self.stepdelay = float(self.EntrySweeptime.get())/self.stepdelay
        self.stepdelay = int(self.stepdelay*1000)
        print("step delay: " + str(self.stepdelay))
        self.SweepLoop()
    
    def StopSweep(self):
        self.Sweeping = False
        
    def SweepLoop(self):
        
        if self.Sweeping == True and self.currentstep < self.SweepEnd:
            if self.Sweeping_bar == 'Master':
                self.masterscaler.set(self.currentstep)
            elif self.Sweeping_bar == 'LED1':
                self.led1scaler.set(self.currentstep)
            elif self.Sweeping_bar == 'LED2':
                self.led2scaler.set(self.currentstep)
            elif self.Sweeping_bar == 'Heater':
                self.heaterscaler.set(self.currentstep)
            else:
                self.Sweeping = False
                print("error")
            self.currentstep += self.SweepStepSize
            self.top.after(self.stepdelay, self.SweepLoop)
        else:
            self.Sweeping = False
        
    def Exit(self):
        self.top.destroy()