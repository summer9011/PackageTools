#!/usr/bin/env python
import wx
import wx.grid
import PTModuleHelper
from PTDBManager import PTDBManager
from PTModuleBranch import PTModuleBranch
from PTModuleBranch import PTRemoteModuleBranch

class PTBranchesFrame (wx.Frame):
    moduleBranchesTable = None

    moduleBranchesData = None
    moduleBranchesBindsData = None

    module = None
    logCallback = None
    callback = None

    def __init__(self, parent, logCallback, callback, module):
        windowSize = wx.DisplaySize()

        size = (600,600)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, parent, wx.ID_ANY, "%s Branches" % module.name, pos=pos, size=size)
        self.SetMinSize(size)

        self.moduleBranchesBindsData = PTDBManager().getModuleBranches(module.id)
        self.module = module
        self.logCallback = logCallback
        self.callback = callback
        self.SetupUI()
        self.refreshBranchesUsingThread()

    def SetupUI(self):
        # Table
        self.moduleBranchesTable = wx.grid.Grid(self, wx.ID_ANY)
        self.moduleBranchesTable.CreateGrid(0, 3, 1)
        self.moduleBranchesTable.SetAutoLayout(1)

        self.moduleBranchesTable.SetColLabelValue(1, u"Remote name")
        self.moduleBranchesTable.SetColSize(0, 160)

        self.moduleBranchesTable.SetColLabelValue(2, u"Bind")
        self.moduleBranchesTable.SetColSize(1, 60)

        self.moduleBranchesTable.SetColLabelValue(3, u"Local path")
        self.moduleBranchesTable.SetColSize(2, 400)

        row = 0
        for moduleRemoteBranch in self.moduleBranchesData:
            self.AppendModuleBranch(row, moduleRemoteBranch)
            row+=1

        self.Show(True)

    def AppendModuleBranch(self, row, moduleRemoteBranch):
        bindInfo = self.GetBindInfoWithRemoteName(moduleRemoteBranch.remoteName)

        self.moduleBranchesTable.AppendRows(1)

        self.moduleBranchesTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.moduleBranchesTable.SetRowSize(row, 30)

        self.moduleBranchesTable.SetCellValue(row, 0, "%d" % moduleRemoteBranch.remoteName)
        self.moduleBranchesTable.SetReadOnly(row, 0)
        self.moduleBranchesTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        isBind = "No"
        if bindInfo != None:
            isBind = "Yes"
        self.moduleBranchesTable.SetCellValue(row, 1, isBind)
        self.moduleBranchesTable.SetReadOnly(row, 1)
        self.moduleBranchesTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        localPath = ""
        if bindInfo != None:
            localPath = bindInfo.localPath
        self.moduleBranchesTable.SetCellValue(row, 2, localPath)
        self.moduleBranchesTable.SetReadOnly(row, 2)
        self.moduleBranchesTable.SetCellAlignment(row, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def GetBindInfoWithRemoteName(self, remoteName):
        findBindInfo = None
        for bindInfo in self.moduleBranchesBindsData:
            if bindInfo.remoteName == remoteName:
                findBindInfo = bindInfo
                break
        return findBindInfo

    def refreshBranchesUsingThread(self):
        PTModuleHelper.getModuleRemoteBranches(self.module, self.logCallback, self.getModuleBranchesCallback)

    def getModuleBranchesCallback(self, remoteBranchesList):
        self.moduleBranchesData = []
        if remoteBranchesList != None:
            self.moduleBranchesData = remoteBranchesList
