#!/usr/bin/env python
import wx
import wx.grid
import PTModuleHelper
from PTDBManager import PTDBManager
from PTCommand import PTCommand

class PTModuleWindow (wx.Window):
    moduleTable = None

    refreshVersionBtn = None
    addModuleBtn = None
    deleteModuleBtn = None
    publishBtn = None

    moduleData = None

    logCallback = None
    addModuleCallback = None

    def __init__(self, parent, logCallback, addModuleCallback):
        wx.Window.__init__(self, parent)

        self.moduleData = PTDBManager().getModuleList()
        self.logCallback = logCallback
        self.addModuleCallback = addModuleCallback
        self.SetupUI()
        self.refreshVersionsUsingThread()

    def SetupUI(self):
        # Table
        self.moduleTable = wx.grid.Grid(self, wx.ID_ANY)
        self.moduleTable.CreateGrid(0, 6, 1)
        self.moduleTable.SetAutoLayout(1)

        self.moduleTable.SetColLabelValue(0, u"ID")
        self.moduleTable.SetColSize(0, 60)

        self.moduleTable.SetColLabelValue(1, u"Module name")
        self.moduleTable.SetColSize(1, 160)

        self.moduleTable.SetColLabelValue(2, u"Code repo name")
        self.moduleTable.SetColSize(2, 160)

        self.moduleTable.SetColLabelValue(3, u"Spec repo name")
        self.moduleTable.SetColSize(3, 160)

        self.moduleTable.SetColLabelValue(4, u"Local version")
        self.moduleTable.SetColSize(4, 120)

        self.moduleTable.SetColLabelValue(5, u"Remote version")
        self.moduleTable.SetColSize(5, 120)

        row = 0
        for module in self.moduleData:
            self.AppendModule(row, module)
            row+=1

        self.moduleTable.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.moduleTable.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

        # Btns
        self.refreshVersionBtn = wx.Button(self, wx.ID_ANY, u"Refresh versions")
        self.refreshVersionBtn.Bind(wx.EVT_BUTTON, self.OnRefreshVersion)

        self.addModuleBtn = wx.Button(self, wx.ID_ANY, u"Add Module")
        self.addModuleBtn.Bind(wx.EVT_BUTTON, self.OnAddModule)

        self.publishBtn = wx.Button(self, wx.ID_ANY, u"Publish")
        self.publishBtn.Bind(wx.EVT_BUTTON, self.OnPublishModule)
        self.publishBtn.Enable(False)

        self.deleteModuleBtn = wx.Button(self, wx.ID_ANY, u"Delete")
        self.deleteModuleBtn.Bind(wx.EVT_BUTTON, self.OnDeleteModule)
        self.deleteModuleBtn.Enable(False)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.refreshVersionBtn, 0, wx.LEFT, 10)
        hBox.Add(self.addModuleBtn, 0, wx.LEFT, 10)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.publishBtn, 0, wx.RIGHT, 10)
        hBox.Add(self.deleteModuleBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.moduleTable, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Fit()

    def AppendModule(self, row, module):
        codeRepo = PTDBManager().getCodeRepo(module.codeRepoId)
        specRepo = PTDBManager().getSpecRepo(module.specRepoId)

        self.moduleTable.AppendRows(1)

        self.moduleTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.moduleTable.SetRowSize(row, 30)

        self.moduleTable.SetCellValue(row, 0, "%d" % module.id)
        self.moduleTable.SetReadOnly(row, 0)
        self.moduleTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleTable.SetCellValue(row, 1, module.name)
        self.moduleTable.SetReadOnly(row, 1)
        self.moduleTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleTable.SetCellValue(row, 2, codeRepo.name)
        self.moduleTable.SetReadOnly(row, 2)
        self.moduleTable.SetCellAlignment(row, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleTable.SetCellValue(row, 3, specRepo.name)
        self.moduleTable.SetReadOnly(row, 3)
        self.moduleTable.SetCellAlignment(row, 3, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleTable.SetCellValue(row, 4, module.localVersion)
        self.moduleTable.SetReadOnly(row, 4)
        self.moduleTable.SetCellAlignment(row, 4, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.moduleTable.SetCellValue(row, 5, module.remoteVersion)
        self.moduleTable.SetReadOnly(row, 5)
        self.moduleTable.SetCellAlignment(row, 5, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.UpdateCellTextColor(row, module)

    def UpdateCellTextColor(self, row, module):
        if module.isNewer():
            self.moduleTable.SetCellTextColour(row, 4, wx.BLUE)
        elif module.isOlder():
            self.moduleTable.SetCellTextColour(row, 4, wx.RED)
        else:
            self.moduleTable.SetCellTextColour(row, 4, wx.BLACK)

    def ClearSelection(self):
        self.moduleTable.ClearSelection()
        self.publishBtn.Enable(False)
        self.deleteModuleBtn.Enable(False)

    def OnRefreshVersion(self, event):
        self.refreshVersionsUsingThread()

    def refreshVersionsUsingThread(self):
        PTModuleHelper.asyncModuleVersions(self.moduleData, self.logCallback, self.refreshVersionCallback)

    def refreshVersionCallback(self, module):
        row = self.moduleData.index(module)
        self.moduleTable.SetCellValue(row, 4, module.localVersion)
        self.moduleTable.SetCellValue(row, 5, module.remoteVersion)
        self.UpdateCellTextColor(row, module)

        if len(self.moduleTable.SelectedRows) > 0 and self.moduleTable.SelectedRows[0] == row:
            self.publishBtn.Enable(module.isNewer())
            self.deleteModuleBtn.Enable(True)
            module.isPublishing = False

    def OnAddModule(self, event):
        self.addModuleCallback()

    def OnDeleteModule(self, event):
        self.refreshVersionBtn.Enable(False)

        row = self.moduleTable.SelectedRows[0]
        module = self.moduleData[row]

        PTDBManager().deleteModule(module)
        self.moduleData.remove(module)
        self.moduleTable.DeleteRows(row)
        self.ClearSelection()

        self.refreshVersionBtn.Enable(True)

    def OnPublishModule(self, event):
        row = self.moduleTable.SelectedRows[0]
        module = self.moduleData[row]
        remoteTrunkVersion = PTModuleHelper.getModuleTrunkRemoteVersion(module, self.logCallback)
        if module.localVersion == remoteTrunkVersion:
            module.isPublishing = True
            self.publishBtn.Enable(False)
            self.publishBtn.SetLabelText(u"Publishing")
            self.deleteModuleBtn.Enable(False)
            self.refreshVersionBtn.Enable(False)
            PTCommand().publishModule(module, self.logCallback, self.OnPublishModuleCompleteCallback)
        else:
            wx.MessageBox(u"Module (%s) local version is %s, remote trunk version is %s" % (
                module.name, module.localVersion, remoteTrunkVersion),
                          u"You should commit all changes using SVN Tools.", wx.OK)

    def OnPublishModuleCompleteCallback(self, result, module):
        if result == True:
            PTModuleHelper.asyncModuleVersions([module], self.logCallback, self.refreshVersionCallback)
            self.refreshVersionBtn.Enable(True)

    def OnCellLeftClick(self, event):
        event.Skip()

        row = event.Row
        self.moduleTable.ClearSelection()
        self.moduleTable.SelectRow(row, True)

        module = self.moduleData[row]
        if module.isPublishing == False:
            self.publishBtn.Enable(module.isNewer())
            self.deleteModuleBtn.Enable(module.isPublishing == False)

    def OnLabelLeftClick(self, event):
        pass

    def addModule(self, module):
        self.ClearSelection()
        self.moduleData.append(module)
        self.AppendModule(len(self.moduleData)-1, module)
        self.refreshVersionsUsingThread()

    def reCreateData(self):
        if len(self.moduleData)> 0:
            self.moduleTable.DeleteRows(0, len(self.moduleData))
            self.moduleTable.ClearSelection()

        self.moduleData = PTDBManager().getModuleList()
        row = 0
        for module in self.moduleData:
            self.AppendModule(row, module)
            row+=1
        self.refreshVersionsUsingThread()