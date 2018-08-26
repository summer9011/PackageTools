#!/usr/bin/env python
import wx
from PTDBManager import PTDBManager
from PTSpecRepo import PTSpecRepo

class PTAddRepoFrame (wx.Frame):
    repoTip = None
    repoNameTextTip = None
    repoNameText = None
    repoPathTextTip = None
    repoPathText = None

    callback = None

    def __init__(self, parent, callback):
        windowSize = wx.DisplaySize()

        size = (600,200)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, parent, wx.ID_ANY, u"Add Pod Spec Repo", pos=pos, size=size)
        self.SetMinSize(size)

        self.callback = callback

        gridSizer = wx.FlexGridSizer(2, 2, 10, 10)

        self.repoNameTextTip = wx.StaticText(self)
        self.repoNameTextTip.SetLabelText(u"Repo name :")
        gridSizer.Add(self.repoNameTextTip, 0)

        self.repoNameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.repoNameText, 1, wx.EXPAND)

        self.repoPathTextTip = wx.StaticText(self)
        self.repoPathTextTip.SetLabelText(u"Repo remote path :")
        gridSizer.Add(self.repoPathTextTip, 0)

        self.repoPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.repoPathText, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddRepo)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 30)
        sizer.Add(self.addBtn, 0, wx.CENTER|wx.BOTTOM, 30)

        self.SetSizer(sizer)
        self.Show(True)

    def OnAddRepo(self, event):
        repo = PTSpecRepo()
        repo.repoName = self.repoNameText.GetValue()
        repo.remotePath = self.repoPathText.GetValue()
        if len(repo.repoName) > 0 and len(repo.remotePath) > 0:
            self.addBtn.Enable(False)
            PTDBManager().addNewSpecRepo(repo, self.AddRepoCallback)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)

    def AddRepoCallback(self, repo):
        self.callback(repo)