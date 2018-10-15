#!/usr/bin/env python
import wx
from tools.PTDBManager import PTDBManager

class PTModifyCodeRepoDialog (wx.Dialog):
    urlTextTip = None
    urlText = None
    nameTextTip = None
    nameText = None
    pwdTextTip = None
    pwdText = None

    modifyBtn = None

    moduleRepo = None
    callback = None

    def __init__(self, parent, moduleRepo, callback):
        super(PTModifyCodeRepoDialog, self).__init__(parent, size=(500, 300))

        self.moduleRepo = moduleRepo
        self.callback = callback

        gridSizer = wx.FlexGridSizer(3, 2, 10, 10)

        self.urlTextTip = wx.StaticText(self)
        self.urlTextTip.SetLabelText(u"URL :")
        gridSizer.Add(self.urlTextTip, 0)

        self.urlText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        self.urlText.SetValue(self.moduleRepo.url)
        self.urlText.Bind(wx.EVT_TEXT, self.OnTextTextChange)
        gridSizer.Add(self.urlText, 1, wx.EXPAND)

        self.nameTextTip = wx.StaticText(self)
        self.nameTextTip.SetLabelText(u"Username :")
        gridSizer.Add(self.nameTextTip, 0)

        self.nameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        self.nameText.SetValue(self.moduleRepo.user)
        self.nameText.Bind(wx.EVT_TEXT, self.OnTextTextChange)
        gridSizer.Add(self.nameText, 1, wx.EXPAND)

        self.pwdTextTip = wx.StaticText(self)
        self.pwdTextTip.SetLabelText(u"Password :")
        gridSizer.Add(self.pwdTextTip, 0)

        self.pwdText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        self.pwdText.SetValue(self.moduleRepo.pwd)
        self.pwdText.Bind(wx.EVT_TEXT, self.OnTextTextChange)
        gridSizer.Add(self.pwdText, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND | wx.ALL, 30)

        self.modifyBtn = wx.Button(self, wx.ID_ANY, u"Modify")
        self.modifyBtn.Bind(wx.EVT_BUTTON, self.OnModifyRepo)
        self.modifyBtn.Enable(False)

        cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(cancelBtn)
        b.Add((10, 0))
        b.Add(self.modifyBtn)
        sizer.Add(b, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 30)

        self.SetSizer(sizer)

    def OnTextTextChange(self, event):
        url = self.urlText.GetValue()
        name = self.nameText.GetValue()
        pwd = self.pwdText.GetValue()
        enable = (url != self.moduleRepo.url or name != self.moduleRepo.user or pwd != self.moduleRepo.pwd)
        self.modifyBtn.Enable(enable)

    def OnModifyRepo(self, event):
        url = self.urlText.GetValue()
        name = self.nameText.GetValue()
        pwd = self.pwdText.GetValue()
        if len(url) > 0 and len(name) > 0 and len(pwd) > 0:
            self.moduleRepo.url = url
            self.moduleRepo.user = name
            self.moduleRepo.pwd = pwd

            PTDBManager().updateModuleRepoInfo(self.moduleRepo)
            self.callback(self.moduleRepo)
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)

    def OnCancelAction(self, event):
        self.EndModal(wx.ID_OK)