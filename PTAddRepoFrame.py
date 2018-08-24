#!/usr/bin/env python
import wx
import os
from PTDBManager import PTDBManager
from PTSpecRepo import PTSpecRepo

class PTAddRepoFrame (wx.Frame):
    repoTip = None
    repoNameTextTip = None
    repoNameText = None
    repoPathTextTip = None
    repoPathText = None

    callback = None

    def __init__(self, callback):
        windowSize = wx.DisplaySize()

        size = (600,300)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Add Pod Spec Repo", pos=pos, size=size)

        # Local path
        self.repoTip = wx.StaticText(self)
        self.repoTip.SetLabelText(u"Repo info :")
        tipBox = wx.BoxSizer(wx.HORIZONTAL)
        tipBox.Add((10, 0))
        tipBox.Add(self.repoTip, flag=wx.ALIGN_LEFT)

        self.repoNameTextTip = wx.StaticText(self)
        self.repoNameTextTip.SetLabelText(u"Repo name :")
        self.repoNameText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        nameBox.Add((10, 0))
        nameBox.Add(self.repoNameTextTip, 0, wx.TE_LEFT)
        nameBox.Add((10, 0))
        nameBox.Add(self.repoNameText, flag=wx.ALIGN_RIGHT)
        nameBox.Add((10, 0))

        self.repoPathTextTip = wx.StaticText(self)
        self.repoPathTextTip.SetLabelText(u"Repo remote path :")
        self.repoPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        pathBox = wx.BoxSizer(wx.HORIZONTAL)
        pathBox.Add((10, 0))
        pathBox.Add(self.repoPathTextTip, 0, wx.TE_LEFT)
        pathBox.Add((10, 0))
        pathBox.Add(self.repoPathText, flag=wx.ALIGN_RIGHT)
        pathBox.Add((10, 0))

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddRepo)
        addBtnBox = wx.BoxSizer(wx.HORIZONTAL)
        addBtnBox.Add(self.addBtn, 0, wx.TE_CENTER)

        vboxer = wx.BoxSizer(wx.VERTICAL)
        vboxer.Add((0, 20))
        vboxer.Add(tipBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 10))
        vboxer.Add(nameBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 20))
        vboxer.Add(pathBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0, 30))
        vboxer.Add(addBtnBox, flag=wx.ALIGN_CENTER)

        self.SetSizer(vboxer)
        self.Show(True)

        self.callback = callback

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
        if self.callback != None:
            self.callback(repo)