#!/usr/bin/env python
import wx
from PTCommand import PTCommand

class PTEnvironmentWindow (wx.Window):
    checkPodCommandBtn = None

    logCallback = None

    def __init__(self, parent, logCallback):
        wx.Window.__init__(self, parent)
        self.logCallback = logCallback
        self.SetupUI()

    def SetupUI(self):
        self.checkPodCommandBtn = wx.Button(self, wx.ID_ANY, u"Check `Pod` Command")
        self.checkPodCommandBtn.Bind(wx.EVT_BUTTON, self.OnCheckPodCommand)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.checkPodCommandBtn, 0, wx.LEFT|wx.TOP, 10)

        self.SetSizer(sizer)
        self.Fit()

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