#!/usr/bin/env python
import wx
import wx.dataview
from tools.PTCommand import PTCommand
from tools.PTCommand import PTCommandPathConfig
from views.PTAddSpecRepoDialog import PTAddSpecRepoDialog

class PTSpecRepoFrame (wx.Frame):
    dataListView = None

    addSpecRepoBtn = None
    deleteSpecRepoBtn = None

    addSpecDialog = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTSpecRepoFrame, self).__init__(parent, wx.ID_ANY, u"Podspec Repo List", size=(600, 400))

        self.logCallback = logCallback
        self.SetupUI()

        if PTCommandPathConfig.podspecList == None:
            PTCommand().getSpecRepoList(self.logCallback, self.OnGetSpecRepoListCompleteCallback)
        else:
            self.OnSuccessGetSpecRepoList()

        self.CentreOnScreen()
        self.Show(True)

    def OnGetSpecRepoListCompleteCallback(self, specRepoList):
        PTCommandPathConfig.podspecList = specRepoList
        self.OnSuccessGetSpecRepoList()

    def OnSuccessGetSpecRepoList(self):
        for (name, path) in PTCommandPathConfig.podspecList:
            self.dataListView.AppendItem([name, path])

    def SetupUI(self):
        self.dataListView = wx.dataview.DataViewListCtrl(self)
        self.dataListView.AppendTextColumn(u"Name", 0, width=180)
        self.dataListView.AppendTextColumn(u"Remote path", 1, width=320)
        self.dataListView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        # Btns
        self.addSpecRepoBtn = wx.Button(self, wx.ID_ANY, u"Add Spec Repo")
        self.addSpecRepoBtn.Bind(wx.EVT_BUTTON, self.OnAddSpecRepo)

        self.deleteSpecRepoBtn = wx.Button(self, wx.ID_ANY, u"Delete")
        self.deleteSpecRepoBtn.Bind(wx.EVT_BUTTON, self.OnDeleteSpecRepo)
        self.deleteSpecRepoBtn.Enable(False)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.addSpecRepoBtn, 0, wx.LEFT, 10)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.deleteSpecRepoBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataListView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)

        self.dataListView.SetFocus()

    def DataViewSelectedRow(self, event):
        if self.dataListView.SelectedItemsCount > 0:
            self.deleteSpecRepoBtn.Enable(True)
            return
        self.deleteSpecRepoBtn.Enable(False)

    def ClearSelection(self):
        self.dataListView.UnselectAll()
        self.deleteSpecRepoBtn.Enable(False)

    def OnAddSpecRepo(self, event):
        self.addSpecDialog = PTAddSpecRepoDialog(self, self.logCallback, self.OnAddSpecRepoCompleteCallback)
        self.addSpecDialog.ShowWindowModal()

    def OnDeleteSpecRepo(self, event):
        item = self.dataListView.Selection
        if item != None:
            row = self.dataListView.ItemToRow(item)
            specRepo = PTCommandPathConfig.podspecList[row]
            PTCommand().removeSpecRepo(specRepo[0], self.logCallback, self.OnDeleteSpecRepoCompleteCallback)

    def OnDeleteSpecRepoCompleteCallback(self, name):
        item = self.dataListView.Selection
        row = self.dataListView.ItemToRow(item)
        specRepo = PTCommandPathConfig.podspecList[row]

        PTCommandPathConfig.podspecList.remove(specRepo)
        self.dataListView.DeleteItem(row)
        self.ClearSelection()

    def OnAddSpecRepoCompleteCallback(self, name, remotePath):
        self.addSpecDialog.EndModal(0)
        self.addSpecRepo(name, remotePath)

    def addSpecRepo(self, name, remotePath):
        self.ClearSelection()
        PTCommandPathConfig.podspecList.append((name, remotePath))
        self.dataListView.AppendItem([name, remotePath])