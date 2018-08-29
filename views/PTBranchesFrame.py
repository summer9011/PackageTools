#!/usr/bin/env python
import wx
import os
import wx.grid
from tools import PTModuleHelper
from tools.PTDBManager import PTDBManager
from models.PTModuleBranch import PTModuleBranch
from tools.PTCommand import PTCommand
from models.PTModule import PTModule

class PTBranchesFrame (wx.Frame):
    moduleBranchesTable = None

    refreshBranchesBtn = None
    bindBtn = None
    publishBtn = None

    moduleBranchesData = []
    moduleBranchesBindsData = None

    module = None
    logCallback = None

    def __init__(self, parent, logCallback, module):
        windowSize = wx.DisplaySize()

        size = (800,500)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, parent, wx.ID_ANY, "%s Branches" % module.name, pos=pos, size=size)
        self.SetBackgroundColour(wx.WHITE)
        self.SetMinSize(size)

        self.moduleBranchesBindsData = PTDBManager().getModuleBranches(module.id)
        self.module = module
        self.logCallback = logCallback
        self.SetupUI()
        self.refreshBranchesUsingThread()

    def SetupUI(self):
        # Table
        self.moduleBranchesTable = wx.grid.Grid(self, wx.ID_ANY)
        self.moduleBranchesTable.CreateGrid(0, 5, 1)
        self.moduleBranchesTable.SetAutoLayout(1)

        self.moduleBranchesTable.SetColLabelValue(0, u"Remote name")
        self.moduleBranchesTable.SetColSize(0, 240)

        self.moduleBranchesTable.SetColLabelValue(1, u"Version")
        self.moduleBranchesTable.SetColSize(1, 60)

        self.moduleBranchesTable.SetColLabelValue(2, u"Bind")
        self.moduleBranchesTable.SetColSize(2, 60)

        self.moduleBranchesTable.SetColLabelValue(3, u"Local version")
        self.moduleBranchesTable.SetColSize(3, 100)

        self.moduleBranchesTable.SetColLabelValue(4, u"Local path")
        self.moduleBranchesTable.SetColSize(4, 340)

        row = 0
        for moduleRemoteBranch in self.moduleBranchesData:
            self.AppendModuleBranch(row, moduleRemoteBranch)
            row+=1

        self.moduleBranchesTable.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.moduleBranchesTable.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

        # Btns
        self.refreshBranchesBtn = wx.Button(self, wx.ID_ANY, u"Refresh branches")
        self.refreshBranchesBtn.Bind(wx.EVT_BUTTON, self.OnRefreshBranches)

        self.bindBtn = wx.Button(self, wx.ID_ANY, u"Bind")
        self.bindBtn.Bind(wx.EVT_BUTTON, self.OnBindBranch)
        self.bindBtn.Enable(False)

        self.publishBtn = wx.Button(self, wx.ID_ANY, u"Publish")
        self.publishBtn.Bind(wx.EVT_BUTTON, self.OnPublishBranch)
        self.publishBtn.Enable(False)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.refreshBranchesBtn, 0, wx.LEFT, 10)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.bindBtn, 0, wx.RIGHT, 10)
        hBox.Add(self.publishBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.moduleBranchesTable, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Fit()

        self.Show(True)

    def AppendModuleBranch(self, row, moduleRemoteBranch):
        bindInfo = self.GetBindInfoWithRemoteName(moduleRemoteBranch.remoteName)
        bindInfo.localVersion = PTModuleHelper.getBranchLocalVersion(bindInfo, self.logCallback)

        self.moduleBranchesTable.AppendRows(1)

        self.moduleBranchesTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.moduleBranchesTable.SetRowSize(row, 30)

        self.moduleBranchesTable.SetCellValue(row, 0, moduleRemoteBranch.remoteName)
        self.moduleBranchesTable.SetReadOnly(row, 0)
        self.moduleBranchesTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleBranchesTable.SetCellValue(row, 1, moduleRemoteBranch.version)
        self.moduleBranchesTable.SetReadOnly(row, 1)
        self.moduleBranchesTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        isBind = "No"
        if bindInfo != None:
            isBind = "Yes"
        self.moduleBranchesTable.SetCellValue(row, 2, isBind)
        self.moduleBranchesTable.SetReadOnly(row, 2)
        self.moduleBranchesTable.SetCellAlignment(row, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleBranchesTable.SetCellValue(row, 3, bindInfo.localVersion)
        self.moduleBranchesTable.SetReadOnly(row, 3)
        self.moduleBranchesTable.SetCellAlignment(row, 3, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        localPath = ""
        if bindInfo != None:
            localPath = bindInfo.localPath
        self.moduleBranchesTable.SetCellValue(row, 4, localPath)
        self.moduleBranchesTable.SetReadOnly(row, 4)
        self.moduleBranchesTable.SetCellAlignment(row, 4, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def GetBindInfoWithRemoteName(self, remoteName):
        findBindInfo = None
        for bindInfo in self.moduleBranchesBindsData:
            if bindInfo.remoteName == remoteName:
                findBindInfo = bindInfo
                break
        return findBindInfo

    def GetBranchInfoWithRemoteName(self, remoteName):
        findBranchInfo = None
        for branchInfo in self.moduleBranchesData:
            if branchInfo.remoteName == remoteName:
                findBranchInfo = branchInfo
                break
        return findBranchInfo

    def OnCellLeftClick(self, event):
        event.Skip()

        row = event.Row
        self.moduleBranchesTable.ClearSelection()
        self.moduleBranchesTable.SelectRow(row, True)

        branchInfo = self.moduleBranchesData[row]
        bindInfo = self.GetBindInfoWithRemoteName(branchInfo.remoteName)
        self.publishBtn.Enable(bindInfo != None)
        self.bindBtn.Enable(True)
        if bindInfo != None:
            self.bindBtn.SetLabelText("Unbind")
        else:
            self.bindBtn.SetLabelText("Bind")

    def OnLabelLeftClick(self, event):
        pass

    def OnRefreshBranches(self, event):
        self.refreshBranchesUsingThread()

    def OnBindBranch(self, event):
        row = self.moduleBranchesTable.SelectedRows[0]
        branchInfo = self.moduleBranchesData[row]
        bindInfo = self.GetBindInfoWithRemoteName(branchInfo.remoteName)
        if bindInfo != None:
            PTDBManager().deleteModuleBranch(bindInfo)
            self.moduleBranchesBindsData.remove(bindInfo)
            self.moduleBranchesTable.SetCellValue(row, 2, "No")
            self.moduleBranchesTable.SetCellValue(row, 3, "")
            self.moduleBranchesTable.SetCellValue(row, 4, "")
            self.bindBtn.SetLabelText("Bind")
            self.publishBtn.Enable(False)
        else:
            dirDlg = wx.DirDialog(self, u"Choose directory", os.path.expanduser('~'), wx.DD_DEFAULT_STYLE)
            if dirDlg.ShowModal() == wx.ID_OK:
                info = PTModuleBranch()
                info.remoteName = branchInfo.remoteName
                info.localPath = dirDlg.GetPath()
                info.moduleId = self.module.id
                info.localVersion = PTModuleHelper.getBranchLocalVersion(info, self.logCallback)
                PTDBManager().addNewModuleBranch(info, self.OnBindBranchCallback)

    def OnBindBranchCallback(self, bindInfo):
        self.moduleBranchesBindsData.append(bindInfo)
        branchInfo = self.GetBranchInfoWithRemoteName(bindInfo.remoteName)
        if branchInfo != None:
            row = self.moduleBranchesData.index(branchInfo)
            self.moduleBranchesTable.SetCellValue(row, 2, "Yes")
            self.moduleBranchesTable.SetCellValue(row, 3, bindInfo.localVersion)
            self.moduleBranchesTable.SetCellValue(row, 4, bindInfo.localPath)
            self.bindBtn.SetLabelText("Unbind")
            self.publishBtn.Enable(True)

    def OnPublishBranch(self, event):
        row = self.moduleBranchesTable.SelectedRows[0]
        branchInfo = self.moduleBranchesData[row]
        bindInfo = self.GetBindInfoWithRemoteName(branchInfo.remoteName)

        remoteBranchVersion = branchInfo.version
        if bindInfo.localVersion == remoteBranchVersion:
            remoteTagLastVersion = self.module.remoteVersion
            if PTModule.checkVersionBigger(remoteBranchVersion, remoteTagLastVersion):
                PTCommand().publishModuleBranch(self.module, branchInfo, bindInfo, self.logCallback, self.OnPublishBranchCompleteCallback)
            else:
                wx.MessageBox(u"Module (%s) branch \"%s\" version must bigger version %s" % (
                    self.module.name, branchInfo.remoteName, remoteTagLastVersion),
                              u"You should change your version string, commit the change.", wx.OK)
        else:
            wx.MessageBox(u"Module (%s) branch %s local version is %s, remote branch version is %s" % (
                self.module.name, branchInfo.remoteName, bindInfo.localVersion, remoteBranchVersion),
                          u"You should commit all changes using SVN Tools.", wx.OK)

    def OnPublishBranchCompleteCallback(self, bindInfo):
        self.refreshBranchesUsingThread()

    def refreshBranchesUsingThread(self):
        PTModuleHelper.getModuleRemoteBranches(self.module, self.logCallback, self.getModuleBranchesCallback)

    def getModuleBranchesCallback(self, remoteBranchesList):
        if len(self.moduleBranchesData) > 0:
            self.moduleBranchesTable.DeleteRows(0, len(self.moduleBranchesData))
            self.moduleBranchesTable.ClearSelection()

        self.moduleBranchesData = []
        if remoteBranchesList != None:
            self.moduleBranchesData = remoteBranchesList

        row = 0
        for moduleRemoteBranch in self.moduleBranchesData:
            self.AppendModuleBranch(row, moduleRemoteBranch)
            row+=1
