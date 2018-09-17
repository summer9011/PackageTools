#!/usr/bin/env python
import wx
import wx.dataview

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

    dataViewModel = None

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTModuleWindow, self).__init__(parent)

        self.logCallback = logCallback
        self.SetupUI()

    def CreateDemoData(self):
        #tree1
        m1 = PTModule()
        m1.name = "KioskMakeupUI"
        m1.localVersion = "1.0.0"
        m1.remoteVersion = "1.0.0"

        moduleTree1 = PTModuleTree()
        moduleTree1.name = "Trunk"
        moduleTree1.val = m1

        m2 = PTModule()
        m2.name = "KioskMakeupUI-1"
        m2.localVersion = "1.0.0"
        m2.remoteVersion = "1.0.0"

        moduleTree2 = PTModuleTree()
        moduleTree2.name = m2.name
        moduleTree2.val = m2

        m3 = PTModule()
        m3.name = "KioskMakeupUI-2"
        m3.localVersion = "1.0.0"
        m3.remoteVersion = "1.0.0"

        moduleTree3 = PTModuleTree()
        moduleTree3.name = m3.name
        moduleTree3.val = m3

        tree1 = PTModuleTree()
        tree1.name = m1.name
        tree1.AddChild(moduleTree1)
        tree1.AddChild(moduleTree2)
        tree1.AddChild(moduleTree3)

        #tree2
        m4 = PTModule()
        m4.name = "KioskCoreModule"
        m4.localVersion = "1.2.0"
        m4.remoteVersion = "1.2.0"

        moduleTree4 = PTModuleTree()
        moduleTree4.name = "Trunk"
        moduleTree4.val = m4

        m5 = PTModule()
        m5.name = "KioskCoreModule-1"
        m5.localVersion = "1.2.0"
        m5.remoteVersion = "1.2.0"

        moduleTree5 = PTModuleTree()
        moduleTree5.name = m5.name
        moduleTree5.val = m5

        tree2 = PTModuleTree()
        tree2.name = m4.name
        tree2.AddChild(moduleTree4)
        tree2.AddChild(moduleTree5)

        #root
        root = PTModuleTree.Root()
        root.AddChild(tree1)
        root.AddChild(tree2)

        return root

    def SetupUI(self):
        self.fileDrop = PTFileDrop(self.OnDropFileCallback)
        self.dropBox = wx.StaticBox(self, label=u"*Drag local module here.", size=(0, 100))
        self.dropBox.SetDropTarget(self.fileDrop)

        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendTextColumn(u"Module", 0, width=280)
        self.dataView.AppendTextColumn(u"Version", 1, width=160)
        self.dataView.AppendTextColumn(u"Latest Version", 2, width=160)
        self.dataView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        moduleTree = self.CreateDemoData()
        self.dataViewModel = PTModuleViewModel(moduleTree)
        self.dataView.AssociateModel(self.dataViewModel)
        self.dataViewModel.DecRef()

        for tree in moduleTree.children:
            self.dataView.Expand(self.dataViewModel.ObjectToItem(tree))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.dropBox, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def DataViewSelectedRow(self, event):
        item = event.GetItem()
        if item.GetID() != None:
            print item

    def OnDropFileCallback(self, filepath):
        PTModuleHelper.FindModuleInfo(filepath, self.logCallback, self.FindModuleInfoCallback)

    def FindModuleInfoCallback(self, name, path, version, url, user):
        if name == None:
            wx.MessageBox(u"Can't find module info.", u"Error", wx.OK | wx.ICON_INFORMATION)
        else:
            m = PTModule()
            m.name = name
            m.path = path
            m.localVersion = version



            dlg = PTRepoDialog(self, m, url, user, self.OnAddModuleCallback)
            dlg.ShowWindowModal()

            # id = 0
            # sepcName = ""
            # trunkId = 0
            # repo = None
            # remoteVersion = ""

    def OnAddModuleCallback(self, module, isTrunk):
        print module