#!/usr/bin/env python
import wx
import os
from PTDBManager import PTDBManager
from PTModule import  PTModule

class PTAddSpecFrame (wx.Frame):
    callback = None

    def __init__(self, callback):
        windowSize = wx.DisplaySize()

        size = (600,300)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Add Pod Spec", pos=pos, size=size)


        self.Show(True)

        self.callback = callback