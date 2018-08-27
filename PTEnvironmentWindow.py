#!/usr/bin/env python
import wx
import os
from PTCommand import PTCommand
from PTDBManager import PTDBManager

class PTEnvironmentWindow (wx.Window):
    checkPodCommandBtn = None
    importDataBtn = None
    exportDataBtn = None

    logCallback = None
    importCallback = None

    def __init__(self, parent, logCallback, importCallback):
        wx.Window.__init__(self, parent)
        self.logCallback = logCallback
        self.importCallback = importCallback
        self.SetupUI()

    def SetupUI(self):
        self.checkPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `Pod` Command")
        self.checkPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckPodCommand)

        self.importDataBtn = wx.Button(self, wx.ID_ANY, u"Import Data")
        self.importDataBtn.Bind(wx.EVT_BUTTON, self.OnImportData)

        self.exportDataBtn = wx.Button(self, wx.ID_ANY, u"Export Data")
        self.exportDataBtn.Bind(wx.EVT_BUTTON, self.OnExportData)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.checkPodCommandBtn, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.importDataBtn, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.exportDataBtn, 0, wx.LEFT|wx.TOP, 10)

        self.SetSizer(sizer)
        self.Fit()

    # Check pod command
    def OnCheckPodCommand(self, event):
        self.checkPodCommandBtn.Enable(False)
        self.checkPodCommandBtn.SetLabelText(u"Checking")
        PTCommand().checkPodCommand(self.logCallback, self.OnCheckPodCommandCallback)

    def OnCheckPodCommandCallback(self, result):
        self.checkPodCommandBtn.Enable(True)
        if result == True:
            self.checkPodCommandBtn.SetLabelText(u"Check `Pod` Command")
        else:
            self.checkPodCommandBtn.SetLabelText(u"ReCheck")

    # Import data
    def OnImportData(self, event):
        filesFilter = "Dicom (*.json)|*.json|"
        fileDlg = wx.FileDialog(self, u"Choose Json File", os.path.expanduser('~'), wildcard=filesFilter, style=wx.FD_OPEN)
        if fileDlg.ShowModal() == wx.ID_OK:
            self.importDataBtn.Enable(False)
            self.importDataBtn.SetLabelText(u"Importing")
            PTDBManager().importData(fileDlg.GetPath(), self.OnImportDataCallback)

    def OnImportDataCallback(self, result):
        self.importDataBtn.Enable(True)
        self.importDataBtn.SetLabelText(u"Import Data")
        self.importCallback()

    # Export data
    def OnExportData(self, event):
        filesFilter = "Dicom (*.json)|*.json|"
        fileDlg = wx.FileDialog(self, u"Save Json File", os.path.expanduser('~'), wildcard=filesFilter, style=wx.FD_SAVE)
        if fileDlg.ShowModal() == wx.ID_OK:
            self.exportDataBtn.Enable(False)
            self.exportDataBtn.SetLabelText(u"Exporting")
            PTDBManager().exportData(fileDlg.GetPath(), self.OnExportDataCallback)

    def OnExportDataCallback(self, result):
        self.exportDataBtn.Enable(True)
        self.exportDataBtn.SetLabelText(u"Export Data")