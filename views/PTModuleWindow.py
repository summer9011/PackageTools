#!/usr/bin/env python
import wx
import wx.dataview
import os

from tools import PTModuleHelper
from tools.PTDBManager import PTDBManager
from tools.PTCommand import PTCommand
from PTFileDrop import PTFileDrop
from models.PTModuleViewModel import PTModuleViewModel
from models.PTModuleViewModel import PTModuleTree
from models.PTModule import PTModule
from models.PTModule import PTModuleRepo
from PTRepoDialog import PTRepoDialog

class PTModuleWindow (wx.Window):
    dropBox = None
    dataView = None
    fileDrop = None

    refreshBtn = None
    publishBtn = None
    deleteBtn = None

    moduleTree = None
    dataViewModel = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTModuleWindow, self).__init__(parent)

        self.logCallback = logCallback
        self.CreateModuleTree()
        self.SetupUI()
        self.UpdateDataView()
        self.RefreshModuleVersions()

    def CreateModuleTree(self):
        moduleList = PTDBManager().getModuleList(self.logCallback)
        for module in moduleList:
            self.AddModuleInTree(module)

    def AddModuleInTree(self, module):
        if self.moduleTree == None:
            self.moduleTree = PTModuleTree.Root()

        if module.trunkId == 0:
            name = module.name
            mName = "Trunk"
        else:
            name = module.trunkName
            mName = "Branch \""+module.name+"\""

        foundTree = None
        for tree in self.moduleTree.children:
            if tree.name == name:
                foundTree = tree
                break

        if foundTree == None:
            foundTree = PTModuleTree()
            self.moduleTree.AddChild(foundTree)
        foundTree.name = name

        foundM = None
        for m in foundTree.children:
            if m.name == mName:
                foundM = m
                break

        if foundM == None:
            foundM = PTModuleTree()
            foundTree.AddChild(foundM)
        foundM.name = mName
        foundM.val = module

    def DeleteModuleInTree(self, mTree):
        if self.moduleTree != None:
            removeTree = None
            for tree in self.moduleTree.children:
                if tree.name == mTree.val.trunkName:
                    tree.children.remove(mTree)
                    if len(tree.children) == 0:
                        removeTree = tree
                    break
            if removeTree != None:
                self.moduleTree.children.remove(removeTree)

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.", size=(0, 100))
        self.dropBox.SetDropTarget(self.fileDrop)

        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendTextColumn(u"Module", 0, width=280)
        self.dataView.AppendTextColumn(u"Version", 1, width=160)
        self.dataView.AppendTextColumn(u"Latest Version", 2, width=160)
        self.dataView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        self.refreshBtn = wx.Button(self, wx.ID_ANY, u"Refresh versions")
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshVersions)

        self.publishBtn = wx.Button(self, wx.ID_ANY, u"Publish module")
        self.publishBtn.Bind(wx.EVT_BUTTON, self.OnPublishVersion)
        self.publishBtn.Enable(False)

        self.deleteBtn = wx.Button(self, wx.ID_ANY, u"Delete module")
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteVersion)
        self.deleteBtn.Enable(False)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(self.refreshBtn, 0, wx.RIGHT, 30)
        b.Add(self.publishBtn, 0, wx.RIGHT, 30)
        b.Add(self.deleteBtn, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.dropBox, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def OnRefreshVersions(self, event):
        self.RefreshModuleVersions()

    def OnPublishVersion(self, event):
        item = self.dataView.Selection
        m = self.dataViewModel.ItemToObject(item)
        print(m)

    def OnDeleteVersion(self, event):
        item = self.dataView.Selection
        m = self.dataViewModel.ItemToObject(item)
        PTDBManager().deleteModule(m.val)
        self.DeleteModuleInTree(m)
        self.UpdateDataView()

    def UpdateDataView(self):
        if self.moduleTree != None:
            self.dataViewModel = PTModuleViewModel(self.moduleTree)
            self.dataView.AssociateModel(self.dataViewModel)
            self.dataViewModel.DecRef()

            for tree in self.moduleTree.children:
                self.dataView.Expand(self.dataViewModel.ObjectToItem(tree))

    def RefreshModuleVersions(self):
        mTrees = []
        for tree in self.moduleTree.children:
            for mTree in tree.children:
                mTrees.append(mTree)
        PTModuleHelper.asyncModuleVersions(mTrees, self.logCallback, self.RefreshModuleVersionsCallback)

    def RefreshModuleVersionsCallback(self, mTree):
        item = self.dataViewModel.ObjectToItem(mTree)
        self.dataViewModel.ChangeValue(mTree.val.localVersion, item, 1)
        self.dataViewModel.ChangeValue(mTree.val.remoteVersion, item, 2)

    def DataViewSelectedRow(self, event):
        item = event.GetItem()
        if item.GetID() != None:
            obj = self.dataViewModel.ItemToObject(item)
            if obj.val != None:
                self.publishBtn.Enable(True)
                self.deleteBtn.Enable(True)
                return

        self.publishBtn.Enable(False)
        self.deleteBtn.Enable(False)

    def OnDropFileCallback(self, filepath):
        PTModuleHelper.FindModuleInfo(filepath, self.logCallback, self.FindModuleInfoCallback)

    def FindModuleInfoCallback(self, trunkName, path, version, url, user):
        if trunkName == None:
            wx.MessageBox(u"Can't find module info.", u"Error", wx.OK | wx.ICON_INFORMATION)
        else:
            m = PTModule()
            m.name = os.path.basename(path)
            m.trunkName = trunkName
            m.path = path
            m.localVersion = version

            urlArr = url.split("/")
            urlArr.pop()
            dlg = PTRepoDialog(self, m, "/".join(urlArr), user, self.OnAddModuleCallback)
            dlg.ShowWindowModal()

    def OnAddModuleCallback(self, module, isTrunk):
        if isTrunk == True:
            PTDBManager().addNewTrunkModule(module)
        else:
            PTDBManager().addNewBranchModule(module)
        self.AddModuleInView(module)

    def AddModuleInView(self, module):
        self.AddModuleInTree(module)
        self.UpdateDataView()
        self.RefreshModuleVersions()