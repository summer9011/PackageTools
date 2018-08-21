#!/usr/bin/env python
import wx
import os
from PTDBManager import PTDBManager
from PTModule import  PTModule

class PTAddModuleFrame (wx.Frame):
    localPathTip = None
    localPathText = None
    localPathBtn = None

    remotePathTip = None
    remotePathTextTip = None
    remotePathText = None
    remotePathUserTip = None
    remotePathUser = None
    remotePathPwdTip = None
    remotePathPwd = None

    addBtn = None

    callback = None

    def __init__(self, callback):
        windowSize = wx.DisplaySize()

        size = (600,300)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Add module", pos=pos, size=size)

        # Local path
        self.localPathTip = wx.StaticText(self)
        self.localPathTip.SetLabelText(u"Local module path :")
        tipBox = wx.BoxSizer(wx.HORIZONTAL)
        tipBox.Add((10, 0))
        tipBox.Add(self.localPathTip, flag=wx.ALIGN_LEFT)

        self.localPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_READONLY,size=(400, 22))
        self.localPathBtn = wx.Button(self, wx.ID_ANY, u"Choose")
        self.localPathBtn.Bind(wx.EVT_BUTTON, self.OnChooseDirectory)
        inputBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.Add((10, 0))
        inputBox.Add(self.localPathText, 0, wx.TE_LEFT)
        inputBox.Add((10, 0))
        inputBox.Add(self.localPathBtn, flag=wx.ALIGN_RIGHT)
        inputBox.Add((10, 0))

        # Remote path
        self.remotePathTip = wx.StaticText(self)
        self.remotePathTip.SetLabelText(u"Remote module path :")
        tipBox2 = wx.BoxSizer(wx.HORIZONTAL)
        tipBox2.Add((10, 0))
        tipBox2.Add(self.remotePathTip, flag=wx.ALIGN_LEFT)

        self.remotePathTextTip = wx.StaticText(self)
        self.remotePathTextTip.SetLabelText(u"URL(https:||http:|svn:) :")
        self.remotePathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(400, 22))
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        textBox.Add((10, 0))
        textBox.Add(self.remotePathTextTip, 0, wx.TE_LEFT)
        textBox.Add((10, 0))
        textBox.Add(self.remotePathText, flag=wx.ALIGN_RIGHT)
        textBox.Add((10, 0))

        self.remotePathUserTip = wx.StaticText(self)
        self.remotePathUserTip.SetLabelText(u"Account :")
        self.remotePathUser = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        userBox = wx.BoxSizer(wx.HORIZONTAL)
        userBox.Add((10, 0))
        userBox.Add(self.remotePathUserTip, 0, wx.TE_LEFT)
        userBox.Add((10, 0))
        userBox.Add(self.remotePathUser, flag=wx.ALIGN_RIGHT)
        userBox.Add((10, 0))

        self.remotePathPwdTip = wx.StaticText(self)
        self.remotePathPwdTip.SetLabelText(u"Password :")
        self.remotePathPwd = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_PASSWORD,size=(200, 22))
        pwdBox = wx.BoxSizer(wx.HORIZONTAL)
        pwdBox.Add((10, 0))
        pwdBox.Add(self.remotePathPwdTip, 0, wx.TE_LEFT)
        pwdBox.Add((10, 0))
        pwdBox.Add(self.remotePathPwd, flag=wx.ALIGN_RIGHT)
        pwdBox.Add((10, 0))

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddModule)
        addBtnBox = wx.BoxSizer(wx.HORIZONTAL)
        addBtnBox.Add(self.addBtn, 0, wx.TE_CENTER)

        vboxer = wx.BoxSizer(wx.VERTICAL)
        vboxer.Add((0, 20))
        vboxer.Add(tipBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 10))
        vboxer.Add(inputBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 20))
        vboxer.Add(tipBox2, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 10))
        vboxer.Add(textBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 10))
        vboxer.Add(userBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 10))
        vboxer.Add(pwdBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 30))
        vboxer.Add(addBtnBox, flag=wx.ALIGN_CENTER)

        self.SetSizer(vboxer)
        self.Show(True)

        self.callback = callback

    def OnChooseDirectory(self, event):
        dirDlg = wx.DirDialog(self, u"Choose directory", os.path.expanduser('~'), wx.DD_DEFAULT_STYLE)
        if dirDlg.ShowModal() == wx.ID_OK:
            self.localPathText.SetValue(dirDlg.GetPath())

    def OnAddModule(self, event):
        module = PTModule()
        module.localPath = self.localPathText.GetValue()
        module.remotePath = self.remotePathText.GetValue()
        module.username = self.remotePathUser.GetValue()
        module.password = self.remotePathPwd.GetValue()
        module.moduleName = os.path.basename(module.localPath)
        PTDBManager().addNewModule([module], self.AddModuleCallback)

    def AddModuleCallback(self, result):
        if self.callback != None:
            self.callback(result)