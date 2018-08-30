#!/usr/bin/env python
import wx
from tools.PTDBManager import PTDBManager
from models.PTCodeRepo import PTCodeRepo

class PTAddCodeRepoFrame (wx.Frame):
    codeRepoNameTextTip = None
    codeRepoNameText = None
    codeRepoPathTextTip = None
    codeRepoPathText = None
    codeUsernameTextTip = None
    codeUsernameText = None
    codePasswordTextTip = None
    codePasswordText = None
    codeTypeTip = None
    codeTypeChoice = None

    callback = None
    selectedType = None

    def __init__(self, parent, callback):
        super(PTAddCodeRepoFrame, self).__init__(parent, wx.ID_ANY, u"Add Code Repo", size=(600,290))

        self.callback = callback

        gridSizer = wx.FlexGridSizer(5, 2, 10, 10)

        self.codeRepoNameTextTip = wx.StaticText(self)
        self.codeRepoNameTextTip.SetLabelText(u"Name :")
        gridSizer.Add(self.codeRepoNameTextTip, 0)

        self.codeRepoNameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.codeRepoNameText, 1, wx.EXPAND)

        self.codeRepoPathTextTip = wx.StaticText(self)
        self.codeRepoPathTextTip.SetLabelText(u"Remote path :")
        gridSizer.Add(self.codeRepoPathTextTip, 0)

        self.codeRepoPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.codeRepoPathText, 1, wx.EXPAND)

        self.codeUsernameTextTip = wx.StaticText(self)
        self.codeUsernameTextTip.SetLabelText(u"Account :")
        gridSizer.Add(self.codeUsernameTextTip, 0)

        self.codeUsernameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.codeUsernameText, 1, wx.EXPAND)

        self.codePasswordTextTip = wx.StaticText(self)
        self.codePasswordTextTip.SetLabelText(u"Password :")
        gridSizer.Add(self.codePasswordTextTip, 0)

        self.codePasswordText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_PASSWORD,size=(200, 22))
        gridSizer.Add(self.codePasswordText, 1, wx.EXPAND)

        self.codeTypeTip = wx.StaticText(self)
        self.codeTypeTip.SetLabelText(u"Type :")
        gridSizer.Add(self.codeTypeTip, 0)

        typeChoiceList = ['None', 'Svn', 'Git']
        self.codeTypeChoice = wx.Choice(self, wx.ID_ANY, choices=typeChoiceList)
        self.codeTypeChoice.Bind(wx.EVT_CHOICE, self.OnChoiceType)
        gridSizer.Add(self.codeTypeChoice, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddCodeRepo)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 30)
        sizer.Add(self.addBtn, 0, wx.CENTER|wx.BOTTOM, 30)

        self.SetSizer(sizer)
        self.CentreOnParent()
        self.Show(True)

    def OnChoiceType(self, event):
        self.selectedType = event.Selection

    def OnAddCodeRepo(self, event):
        codeRepo = PTCodeRepo()
        codeRepo.name = self.codeRepoNameText.GetValue()
        codeRepo.remotePath = self.codeRepoPathText.GetValue()
        codeRepo.username = self.codeUsernameText.GetValue()
        codeRepo.password = self.codePasswordText.GetValue()
        if self.selectedType != None:
            codeRepo.type = self.selectedType
        else:
            codeRepo.type = 0

        if len(codeRepo.name) > 0 and len(codeRepo.remotePath) > 0 and len(codeRepo.username) > 0 and len(codeRepo.password) > 0 and codeRepo.type > 0:
            self.addBtn.Enable(False)
            PTDBManager().addNewCodeRepo(codeRepo, self.AddCodeRepoCallback)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)

    def AddCodeRepoCallback(self, codeRepo):
        self.callback(codeRepo)