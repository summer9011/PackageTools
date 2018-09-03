#!/usr/bin/env python
import wx
from tools.PTCommand import PTCommand

class PTAddSpecRepoFrame (wx.Frame):
    specRepoNameTextTip = None
    specRepoNameText = None
    specRepoPathTextTip = None
    specRepoPathText = None

    logCallback = None
    callback = None

    def __init__(self, parent, logCallback, callback):
        super(PTAddSpecRepoFrame, self).__init__(parent, wx.ID_ANY, u"Add Pod Spec Repo", size=(600,200))

        self.logCallback = logCallback
        self.callback = callback

        gridSizer = wx.FlexGridSizer(2, 2, 10, 10)

        self.specRepoNameTextTip = wx.StaticText(self)
        self.specRepoNameTextTip.SetLabelText(u"Name :")
        gridSizer.Add(self.specRepoNameTextTip, 0)

        self.specRepoNameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.specRepoNameText, 1, wx.EXPAND)

        self.specRepoPathTextTip = wx.StaticText(self)
        self.specRepoPathTextTip.SetLabelText(u"Remote path :")
        gridSizer.Add(self.specRepoPathTextTip, 0)

        self.specRepoPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.specRepoPathText, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddSpecRepo)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 30)
        sizer.Add(self.addBtn, 0, wx.CENTER|wx.BOTTOM, 30)

        self.SetSizer(sizer)
        self.Show(True)

    def OnAddSpecRepo(self, event):
        name = self.specRepoNameText.GetValue()
        remotePath = self.specRepoPathText.GetValue()
        if len(name) > 0 and len(remotePath) > 0:
            PTCommand().addSpecRepo(name, remotePath, self.logCallback, self.callback)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)