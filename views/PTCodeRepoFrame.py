#!/usr/bin/env python
import wx
import wx.dataview
from tools.PTDBManager import PTDBManager
from PTModifyCodeRepoDialog import PTModifyCodeRepoDialog

class PTCodeRepoFrame (wx.Frame):
    dataListView = None
    modifyCodeRepoBtn = None

    modifyCodeRepoDialog = None

    repoList = None

    logCallback = None
    closeCallback = None

    def __init__(self, parent, logCallback, closeCallback):
        super(PTCodeRepoFrame, self).__init__(parent, wx.ID_ANY, u"Code Repo List", size=(600, 400), style= wx.CLOSE_BOX | wx.SYSTEM_MENU)

        self.logCallback = logCallback
        self.closeCallback = closeCallback

        self.repoList = PTDBManager().getModuleRepoList()

        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        self.closeCallback()

    def SetupUI(self):
        self.dataListView = wx.dataview.DataViewListCtrl(self)
        self.dataListView.AppendTextColumn(u"Remote path", 0, width=300)
        self.dataListView.AppendTextColumn(u"Username", 1, width=120)
        self.dataListView.AppendTextColumn(u"Password", 2, width=120)
        self.dataListView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        for repo in self.repoList:
            self.dataListView.AppendItem([repo.url, repo.user, repo.pwd])

        # Btns
        self.modifyCodeRepoBtn = wx.Button(self, wx.ID_ANY, u"Modify Code Repo")
        self.modifyCodeRepoBtn.Bind(wx.EVT_BUTTON, self.OnModifySpecRepo)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.modifyCodeRepoBtn, 0, wx.LEFT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataListView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        self.SetSizer(sizer)

        self.dataListView.SetFocus()
        self.modifyCodeRepoBtn.Enable(False)

    def DataViewSelectedRow(self, event):
        if self.dataListView.SelectedItemsCount > 0:
            self.modifyCodeRepoBtn.Enable(True)
            return
        self.modifyCodeRepoBtn.Enable(False)

    def ClearSelection(self):
        self.dataListView.UnselectAll()
        self.modifyCodeRepoBtn.Enable(False)

    def OnModifySpecRepo(self, event):
        item = self.dataListView.Selection
        if item != None:
            row = self.dataListView.ItemToRow(item)
            codeRepo = self.repoList[row]

            self.modifyCodeRepoDialog = PTModifyCodeRepoDialog(self, codeRepo, self.OnModifyCodeRepoCompleteCallback)
            self.modifyCodeRepoDialog.ShowWindowModal()

    def OnModifyCodeRepoCompleteCallback(self, moduleRepo):
        item = self.dataListView.Selection
        if item != None:
            row = self.dataListView.ItemToRow(item)
            self.dataListView.SetValue(moduleRepo.url, row, 0)
            self.dataListView.SetValue(moduleRepo.user, row, 1)
            self.dataListView.SetValue(moduleRepo.pwd, row, 2)
            self.ClearSelection()