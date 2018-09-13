#!/usr/bin/env python
import wx
import wx.dataview

from tools import PTModuleHelper
from tools.PTDBManager import PTDBManager
from tools.PTCommand import PTCommand
from PTFileDrop import PTFileDrop
from models.PTModuleModel import PTModuleModel

class PTModuleWindow (wx.Window):
    dropBox = None
    dataView = None
    fileDrop = None

    dataViewModel = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTModuleWindow, self).__init__(parent)

        self.logCallback = logCallback
        self.SetupUI()

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.", size=(0, 100))
        self.dropBox.SetDropTarget(self.fileDrop)

        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendToggleColumn("Module", 0, width=240)
        self.dataView.AppendTextColumn("Version", 1, width=240, align=wx.ALIGN_CENTER)
        self.dataView.AppendTextColumn("Latest Version", 2, width=240, align=wx.ALIGN_CENTER)

        self.dataViewModel = PTModuleModel()
        self.dataView.AssociateModel(self.dataViewModel)
        self.dataViewModel.DecRef()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.dropBox, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def OnDropFileCallback(self, filepath):
        wx.LogMessage(filepath)