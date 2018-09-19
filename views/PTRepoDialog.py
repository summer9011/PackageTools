#!/usr/bin/env python
import wx

from tools.PTDBManager import PTDBManager
from models.PTModule import PTModuleRepo

class PTRepoDialog (wx.Dialog):
    userText = None
    pwdText = None
    trunkRadio = None
    branchRadio = None

    module = None
    callback = None

    def __init__(self, parent, module, url, user, callback):
        height = 130
        needUser = False
        needPwd = False
        repo = PTDBManager().findModuleRepo(url)
        if repo != None:
            if repo.full(user) == False:
                if len(repo.user) == 0 or repo.user != user:
                    needUser = True
                needPwd = True
                height = 260
        else:
            needUser = True
            needPwd = True
            repo = PTModuleRepo()
            repo.url = url
            height = 260

        super(PTRepoDialog, self).__init__(parent, size=(500, height))

        self.module = module
        self.module.repo = repo
        self.callback = callback

        box = wx.BoxSizer(wx.VERTICAL)
        if needUser == True or needPwd == True:
            accountInfo = wx.StaticText(self, wx.ID_ANY, u"Repo Account Info")
            box.Add(accountInfo, 0, wx.ALIGN_CENTER|wx.TOP, 10)

            grid = wx.FlexGridSizer(3, 2, 10, 10)
            grid.AddGrowableCol(1)

            urlInfo1 = wx.StaticText(self, wx.ID_ANY, u"Repo url:")
            grid.Add(urlInfo1, 0, wx.ALIGN_RIGHT|wx.RIGHT, 0)
            urlInfo2 = wx.StaticText(self, wx.ID_ANY, url)
            grid.Add(urlInfo2, 1, wx.EXPAND, 0)

            userInfo = wx.StaticText(self, wx.ID_ANY, u"Name:")
            if needUser == True:
                self.userText = wx.TextCtrl(self, wx.ID_ANY, user)
            else:
                self.userText = wx.TextCtrl(self, wx.ID_ANY, user, style=wx.TE_READONLY)
            grid.Add(userInfo, 0, wx.ALIGN_RIGHT|wx.RIGHT, 0)
            grid.Add(self.userText, 1, wx.EXPAND, 0)

            pwdInfo = wx.StaticText(self, wx.ID_ANY, u"Password:")
            self.pwdText = wx.TextCtrl(self, wx.ID_ANY, u"", style=wx.TE_PASSWORD)
            grid.Add(pwdInfo, 0, wx.ALIGN_RIGHT|wx.RIGHT, 0)
            grid.Add(self.pwdText, 1, wx.EXPAND, 0)

            box.Add(grid, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10)
            box.Add((0, 10))

        moduleInfo = wx.StaticText(self, wx.ID_ANY, u"Module Info")
        box.Add(moduleInfo, 0, wx.ALIGN_CENTER|wx.TOP, 10)

        grid2 = wx.GridSizer(1, 2, 10, 10)
        self.trunkRadio = wx.RadioButton(self, wx.ID_ANY, u"Is Trunk")
        grid2.Add(self.trunkRadio)
        self.branchRadio = wx.RadioButton(self, wx.ID_ANY, u"Is Branch")
        grid2.Add(self.branchRadio)
        self.trunkRadio.SetValue(True)

        box.Add(grid2, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        box.Add((0, 10))

        okBtn = wx.Button(self, wx.ID_ANY, u"OK")
        okBtn.Bind(wx.EVT_BUTTON, self.OnOKAction)

        cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(cancelBtn)
        b.Add((10,0))
        b.Add(okBtn)
        box.Add(b, 0, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT, 10)

        self.SetSizer(box)

    def OnOKAction(self, event):
        if self.userText != None:
            self.module.repo.user = self.userText.GetValue()

        if self.pwdText != None:
            self.module.repo.pwd = self.pwdText.GetValue()

        PTDBManager().updateModuleRepo(self.module.repo)
        if self.trunkRadio.GetValue() == True:
            isTrunk = True
        else:
            isTrunk = False
        self.callback(self.module, isTrunk)
        self.EndModal(wx.ID_OK)

    def OnCancelAction(self, event):
        self.EndModal(wx.ID_OK)