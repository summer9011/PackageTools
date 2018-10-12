#!/usr/bin/env python
import wx
import wx.dataview
import wx.adv
import resources.PTResourcePath as Res
from tools.PTCommand import PTCommand
from tools.PTCommand import PTCommandPathConfig
from views.PTAddSpecRepoDialog import PTAddSpecRepoDialog

class PTSpecRepoFrame (wx.Frame):
    dataListView = None
    loadingCtrl = None
    loadingText = None

    addSpecRepoBtn = None
    deleteSpecRepoBtn = None

    addSpecDialog = None

    logCallback = None
    closeCallback = None

    hBox = None
    lcBox = None

    def __init__(self, parent, logCallback, closeCallback):
        super(PTSpecRepoFrame, self).__init__(parent, wx.ID_ANY, u"Podspec Repo List", size=(600, 400), style= wx.CLOSE_BOX | wx.SYSTEM_MENU)

        self.logCallback = logCallback
        self.closeCallback = closeCallback

        hasList = (PTCommandPathConfig.podspecList != None)
        self.SetupUI(hasList)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        if hasList:
            self.OnSuccessGetSpecRepoList()
        else:
            PTCommand().getSpecRepoList(self.logCallback, self.OnGetSpecRepoListCompleteCallback)

        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        self.closeCallback()

    def OnGetSpecRepoListCompleteCallback(self, specRepoList):
        PTCommandPathConfig.podspecList = specRepoList
        self.OnSuccessGetSpecRepoList()

        self.loadingCtrl.Stop()
        self.loadingCtrl.Hide()
        self.loadingText.Hide()
        sizer = self.GetSizer()
        sizer.Hide(self.lcBox)
        sizer.Show(self.dataListView)
        sizer.Show(self.hBox)
        self.Layout()

    def OnSuccessGetSpecRepoList(self):
        for (name, path) in PTCommandPathConfig.podspecList:
            self.dataListView.AppendItem([name, path])

    def SetupUI(self, hasList):
        self.dataListView = wx.dataview.DataViewListCtrl(self)
        self.dataListView.AppendTextColumn(u"Name", 0, width=180)
        self.dataListView.AppendTextColumn(u"Remote path", 1, width=320)
        self.dataListView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        animation = wx.adv.Animation(Res.getLoadingGif())
        self.loadingCtrl = wx.adv.AnimationCtrl(self, wx.ID_ANY, animation, size=animation.GetSize())
        font = wx.Font()
        font.SetPointSize(36)
        self.loadingText = wx.StaticText(self, wx.ID_ANY, u"Loading...")
        self.loadingText.SetFont(font)
        lBox = wx.BoxSizer(wx.HORIZONTAL)
        lBox.Add(self.loadingCtrl, 0, wx.RIGHT, 10)
        lBox.Add(self.loadingText, 0)

        self.lcBox = wx.BoxSizer(wx.HORIZONTAL)
        self.lcBox.Add(lBox, 0, wx.ALIGN_CENTER)

        # Btns
        self.addSpecRepoBtn = wx.Button(self, wx.ID_ANY, u"Add Spec Repo")
        self.addSpecRepoBtn.Bind(wx.EVT_BUTTON, self.OnAddSpecRepo)

        self.deleteSpecRepoBtn = wx.Button(self, wx.ID_ANY, u"Delete")
        self.deleteSpecRepoBtn.Bind(wx.EVT_BUTTON, self.OnDeleteSpecRepo)
        self.deleteSpecRepoBtn.Enable(False)

        self.hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox.Add(self.addSpecRepoBtn, 0, wx.LEFT, 10)
        self.hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        self.hBox.Add(self.deleteSpecRepoBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataListView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        sizer.Add(self.lcBox, 1, wx.CENTER)

        if hasList == True:
            self.loadingCtrl.Stop()
            self.loadingCtrl.Hide()
            sizer.Hide(self.lcBox)
        else:
            sizer.Hide(self.dataListView)
            sizer.Hide(self.hBox)
            self.loadingCtrl.Show()
            self.loadingCtrl.Play()
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