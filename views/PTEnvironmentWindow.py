#!/usr/bin/env python
import wx
import os
from tools.PTCommand import PTCommand
from tools.PTDBManager import PTDBManager
from models.PTCommandPath import PTCommandPath
from tools.PTCommandPathConfig import PTCommandPathConfig

class PTEnvironmentWindow (wx.Window):
    svnCommandText = None
    setSvnCommandBtn = None
    checkSvnCommandBtn = None

    podCommandText = None
    setPodCommandBtn = None
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
        self.svnCommandText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(280, 22))
        self.svnCommandText.SetValue(PTCommandPathConfig().command("svn"))
        self.setSvnCommandBtn = wx.Button(self, wx.ID_ANY, u"Set `svn` command")
        self.setSvnCommandBtn.Bind(wx.EVT_BUTTON, self.OnSetSvnCommand)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.svnCommandText, 0, wx.RIGHT, 10)
        hBox1.Add(self.setSvnCommandBtn, 0)

        self.checkSvnCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `svn` Command")
        self.checkSvnCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckSvnCommand)

        self.podCommandText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(280, 22))
        self.podCommandText.SetValue(PTCommandPathConfig().command("pod"))
        self.setPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Set `pod` command")
        self.setPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnSetPodCommand)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(self.podCommandText, 0, wx.RIGHT, 10)
        hBox2.Add(self.setPodCommandBtn, 0)

        self.checkPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `pod` Command")
        self.checkPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckPodCommand)

        self.importDataBtn = wx.Button(self, wx.ID_ANY, u"Import Data")
        self.importDataBtn.Bind(wx.EVT_BUTTON, self.OnImportData)

        self.exportDataBtn = wx.Button(self, wx.ID_ANY, u"Export Data")
        self.exportDataBtn.Bind(wx.EVT_BUTTON, self.OnExportData)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.checkSvnCommandBtn, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(hBox1, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.checkPodCommandBtn, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(hBox2, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add((0,30))
        sizer.Add(self.importDataBtn, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.exportDataBtn, 0, wx.LEFT|wx.TOP, 10)

        self.SetSizer(sizer)
        self.Fit()

    # Check svn command
    def OnSetSvnCommand(self, event):
        self.setSvnCommandBtn.Enable(False)
        self.setSvnCommandBtn.SetLabelText(u"Setting")

        commandPath = PTCommandPath()
        commandPath.name = "svn"
        commandPath.commandPath = self.svnCommandText.GetValue()
        PTCommandPathConfig().addCommand(commandPath)

        self.setSvnCommandBtn.Enable(True)
        self.setSvnCommandBtn.SetLabelText(u"Set `svn` command")

    def OnCheckSvnCommand(self, event):
        self.checkSvnCommandBtn.Enable(False)
        self.checkSvnCommandBtn.SetLabelText(u"Checking")
        PTCommand().checkSvnCommand(self.logCallback, self.OnCheckSvnCommandCallback)

    def OnCheckSvnCommandCallback(self, result):
        self.checkSvnCommandBtn.Enable(True)
        if result == True:
            self.checkSvnCommandBtn.SetLabelText(u"Check `svn` Command")
        else:
            self.checkSvnCommandBtn.SetLabelText(u"Recheck")

    # Check pod command
    def OnSetPodCommand(self, event):
        self.setPodCommandBtn.Enable(False)
        self.setPodCommandBtn.SetLabelText(u"Setting")

        commandPath = PTCommandPath()
        commandPath.name = "pod"
        commandPath.commandPath = self.podCommandText.GetValue()
        PTCommandPathConfig().addCommand(commandPath)

        self.setPodCommandBtn.Enable(True)
        self.setPodCommandBtn.SetLabelText(u"Set `pod` command")

    def OnCheckPodCommand(self, event):
        self.checkPodCommandBtn.Enable(False)
        self.checkPodCommandBtn.SetLabelText(u"Checking")
        PTCommand().checkPodCommand(self.logCallback, self.OnCheckPodCommandCallback)

    def OnCheckPodCommandCallback(self, result):
        self.checkPodCommandBtn.Enable(True)
        if result == True:
            self.checkPodCommandBtn.SetLabelText(u"Check `pod` Command")
        else:
            self.checkPodCommandBtn.SetLabelText(u"Recheck")

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