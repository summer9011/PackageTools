#!/usr/bin/env python
import wx
import wx.dataview

from tools import PTModuleHelper
from tools.PTDBManager import PTDBManager
from tools.PTCommand import PTCommand
from PTFileDrop import PTFileDrop

class PTModuleWindow (wx.Window):
    dropBox = None
    dataView = None
    fileDrop = None

    moduleData = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTModuleWindow, self).__init__(parent)

        self.moduleData = PTDBManager().getModuleList()
        self.logCallback = logCallback
        self.SetupUI()

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.", size=(0, 100))
        self.dropBox.SetDropTarget(self.fileDrop)

        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendTextColumn("Name", 0)
        self.dataView.AppendToggleColumn("Path", 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.dropBox, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def OnDropFileCallback(self, filepath):
        wx.LogMessage(filepath)