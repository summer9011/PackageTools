#!/usr/bin/env python
import wx
import wx.dataview
import wx.adv
import resources.PTResourcePath as Res
from tools.PTCommand import PTCommand

from tools import PTModuleHelper
from tools.PTDBManager import PTDBManager
from models.PTModuleViewModel import PTModuleViewModel
from models.PTModuleViewModel import PTModuleTree
from PTVersionDialog import PTVersionDialog
from PTPublishDialog import PTPublishDialog
from PTChooseSpecRepoDialog import PTChooseSpecRepoDialog
from PTDeleteDialog import PTDeleteDialog

class PTModuleWindow (wx.Window):
    dataView = None

    progressDialog = None

    refreshBtn = None
    publishBtn = None
    deleteBtn = None
    updateBtn = None

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
        self.dataView = wx.dataview.DataViewCtrl(self)
        self.dataView.AppendTextColumn(u"Module", 0, width=280)
        self.dataView.AppendTextColumn(u"Version", 1, width=100)
        self.dataView.AppendTextColumn(u"Latest Version", 2, width=100)
        self.dataView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        self.refreshBtn = wx.Button(self, wx.ID_ANY, u"Refresh versions")
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshVersions)

        self.publishBtn = wx.Button(self, wx.ID_ANY, u"Publish module")
        self.publishBtn.Bind(wx.EVT_BUTTON, self.OnPublishVersion)
        self.publishBtn.Enable(False)

        self.deleteBtn = wx.Button(self, wx.ID_ANY, u"Delete module")
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteVersion)
        self.deleteBtn.Enable(False)

        self.updateBtn = wx.Button(self, wx.ID_ANY, u"Update module")
        self.updateBtn.Bind(wx.EVT_BUTTON, self.OnUpdateModule)
        self.updateBtn.Enable(False)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(self.refreshBtn, 0, wx.RIGHT, 30)
        b.Add(self.publishBtn, 0, wx.RIGHT, 30)
        b.Add(self.deleteBtn, 0, wx.RIGHT, 30)
        b.Add(self.updateBtn, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def OnUpdateModule(self, event):
        self.ResetBtnsEnable(False)
        item = self.dataView.Selection
        m = self.dataViewModel.ItemToObject(item)
        PTCommand().svnUpdateModule(m.val, self.logCallback, self.OnUpdateModuleCallback)

    def OnUpdateModuleCallback(self, success, result):
        if success == 0:
            item = self.dataView.Selection
            m = self.dataViewModel.ItemToObject(item)
            PTCommand().svnCheckConflict(m.val, self.logCallback, self.OnCheckConflictCallback)
        else:
            wx.MessageBox(u"Svn update failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
            self.ResetBtnsEnable(True)

    def OnCheckConflictCallback(self, success, result):
        if success == 0:
            conflictFiles = result[1]
            if len(conflictFiles) == 0:
                item = self.dataView.Selection
                m = self.dataViewModel.ItemToObject(item)
                m.val.localVersion = PTModuleHelper.getLocalVersion(m.val.path, self.logCallback)
                self.dataViewModel.ChangeValue(m.val.localVersion, item, 1)
            else:
                wx.MessageBox(u"You have %d conflict files, please solve them.\nConflict files:\n%s" % (len(conflictFiles), conflictFiles), u"Error", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(u"Svn check conflict failed.\n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
        self.ResetBtnsEnable(True)

    def OnRefreshVersions(self, event):
        self.RefreshModuleVersions()

    def OnPublishVersion(self, event):
        item = self.dataView.Selection
        m = self.dataViewModel.ItemToObject(item)
        dialog = PTVersionDialog(self, m.val, self.OnChangeVersionCallback)
        dialog.ShowWindowModal()

    def OnChangeVersionCallback(self, module):
        self.dataViewModel.ChangeValue(module.localVersion, self.dataView.Selection, 1)
        self.progressDialog = PTPublishDialog(self, module, self.logCallback, self.OnChooseRepoCallback, self.OnPublishModuleCallback)
        self.progressDialog.ShowWindowModal()

    def OnChooseRepoCallback(self, module):
        chooseDialog = PTChooseSpecRepoDialog(self, module, self.OnChooseRepoCompleteCallback)
        chooseDialog.Show(True)

    def OnChooseRepoCompleteCallback(self, cancel):
        if cancel == True:
            self.progressDialog.EndModal(0)
            self.ResetBtnsEnable(True)
        else:
            self.progressDialog.ContinueToPublish()

    def OnPublishModuleCallback(self, module):
        self.dataViewModel.ChangeValue(module.remoteVersion, self.dataView.Selection, 2)
        self.ResetBtnsEnable(True)

    def OnDeleteVersion(self, event):
        item = self.dataView.Selection
        m = self.dataViewModel.ItemToObject(item)
        deleteDialog = PTDeleteDialog(self, m.val, self.OnDeleteCompleteCallback)
        deleteDialog.ShowWindowModal()

    def OnDeleteCompleteCallback(self, shouldDelete):
        if shouldDelete == True:
            item = self.dataView.Selection
            m = self.dataViewModel.ItemToObject(item)
            self.dataView.Unselect(item)
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
        self.ResetBtnsEnable(False)
        mTrees = []
        if self.moduleTree != None:
            for tree in self.moduleTree.children:
                for mTree in tree.children:
                    mTrees.append(mTree)
            PTModuleHelper.asyncModuleVersions(mTrees, self.logCallback, self.RefreshModuleVersionsCallback)

    def RefreshModuleVersionsCallback(self, mTree, allDone):
        if allDone == True:
            self.ResetBtnsEnable(True)
        else:
            item = self.dataViewModel.ObjectToItem(mTree)
            self.dataViewModel.ChangeValue(mTree.val.localVersion, item, 1)
            self.dataViewModel.ChangeValue(mTree.val.remoteVersion, item, 2)

    def DataViewSelectedRow(self, event):
        item = event.GetItem()
        if item.GetID() != None:
            obj = self.dataViewModel.ItemToObject(item)
            if obj.val != None:
                self.deleteBtn.Enable(True)
                if obj.val.exist == True:
                    self.publishBtn.Enable(True)
                    self.updateBtn.Enable(True)
                else:
                    self.publishBtn.Enable(False)
                    self.updateBtn.Enable(False)
                return

        self.publishBtn.Enable(False)
        self.deleteBtn.Enable(False)
        self.updateBtn.Enable(False)

    def OnAddModule(self, module, isTrunk):
        if isTrunk == True:
            PTDBManager().addNewTrunkModule(module)
        else:
            PTDBManager().addNewBranchModule(module)
        self.AddModuleInView(module)

    def AddModuleInView(self, module):
        self.AddModuleInTree(module)
        self.UpdateDataView()
        self.RefreshModuleVersions()

    def ResetBtnsEnable(self, enable):
        if enable == True:
            self.refreshBtn.Enable(True)
            if self.dataView.SelectedItemsCount > 0:
                self.publishBtn.Enable(True)
                self.deleteBtn.Enable(True)
                self.updateBtn.Enable(True)
        else:
            self.refreshBtn.Enable(False)
            self.publishBtn.Enable(False)
            self.deleteBtn.Enable(False)
            self.updateBtn.Enable(False)