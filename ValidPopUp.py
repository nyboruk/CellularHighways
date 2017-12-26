# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:04:08 2017

@author: Robyn.Pritchard
"""
from tkinter import *

class ValidPopUp:
    def __init__(self, master):
        self.new = Toplevel()
        master.bind('<y>', self.yes)
        master.bind('<n>', self.no)
        framemain = Frame(self.new, width = 600, height = 500)
        framemain.grid(row = 0, column = 0, padx = 5, pady = 5)
        Label(framemain, text = "Is there an undetected bead in the sort channel?").grid(row = 0, column = 0, columnspan = 2)
        b1 = Button(framemain, text  = "Yes", command = self.yes)
        b1.grid(row = 1, column = 0)
        b2 = Button(framemain, text = "No", command = self.no)
        b2.grid(row = 1, column = 1)

        master.wait_window(self.new)
        
    def yes(self, event = 0):
        self.new.destroy()
        self.result = True
    
    def no(self, event = 0):
        self.new.destroy()
        self.result = False