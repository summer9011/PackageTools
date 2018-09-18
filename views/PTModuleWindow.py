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

    moduleTree = None
    dataViewModel = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTModuleWindow, self).__init__(parent)

        self.logCallback = logCallback
        self.CreateModuleTree()
        self.SetupUI()
        self.UpdateDataView()

    def CreateModuleTree(self):
        moduleList = PTDBManager().getModuleList()
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
            mName = module.name

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

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.", size=(0, 100))
        self.dropBox.SetDropTarget(self.fileDrop)

        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendTextColumn(u"Module", 0, width=280)
        self.dataView.AppendTextColumn(u"Version", 1, width=160)
        self.dataView.AppendTextColumn(u"Latest Version", 2, width=160)
        self.dataView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.dropBox, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def UpdateDataView(self):
        if self.moduleTree != None:
            self.dataViewModel = PTModuleViewModel(self.moduleTree)
            self.dataView.AssociateModel(self.dataViewModel)
            self.dataViewModel.DecRef()

            for tree in self.moduleTree.children:
                self.dataView.Expand(self.dataViewModel.ObjectToItem(tree))

            self.RefreshModuleVersions()

    def RefreshModuleVersions(self):
        print "RefreshModuleVersions"

    def DataViewSelectedRow(self, event):
        item = event.GetItem()
        if item.GetID() != None:
            print item

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