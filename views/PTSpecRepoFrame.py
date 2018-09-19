#!/usr/bin/env python
import wx
import wx.grid
from tools.PTCommand import PTCommand
from views.PTAddSpecRepoDialog import PTAddSpecRepoDialog

class PTSpecRepoFrame (wx.Frame):
    specRepoTable = None

    addSpecRepoBtn = None
    deleteSpecRepoBtn = None

    addSpecDialog = None

    specRepoData = []

    logCallback = None

    def __init__(self, parent, logCallback):
        super(PTSpecRepoFrame, self).__init__(parent, wx.ID_ANY, u"Podspec Repo List", size=(600, 400))

        self.logCallback = logCallback
        self.SetupUI()
        PTCommand().getSpecRepoList(self.logCallback, self.OnGetSpecRepoListCompleteCallback)

        self.CentreOnScreen()
        self.Show(True)

    def OnGetSpecRepoListCompleteCallback(self, specRepoList):
        self.specRepoData = specRepoList

        row = 0
        for specRepo in self.specRepoData:
            self.AppendSpecRepo(row, specRepo)
            row+=1

    def SetupUI(self):
        # Table
        self.specRepoTable = wx.grid.Grid(self, wx.ID_ANY)
        self.specRepoTable.CreateGrid(0, 2, 1)
        self.specRepoTable.SetAutoLayout(1)

        self.specRepoTable.SetColLabelValue(0, u"Name")
        self.specRepoTable.SetColSize(0, 180)

        self.specRepoTable.SetColLabelValue(1, u"Remote path")
        self.specRepoTable.SetColSize(1, 320)

        self.specRepoTable.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.specRepoTable.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

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
        sizer.Add(self.specRepoTable, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)

    def AppendSpecRepo(self, row, specRepo):
        self.specRepoTable.AppendRows(1)

        self.specRepoTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.specRepoTable.SetRowSize(row, 30)

        self.specRepoTable.SetCellValue(row, 0, specRepo[0])
        self.specRepoTable.SetReadOnly(row, 0)
        self.specRepoTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.specRepoTable.SetCellValue(row, 1, specRepo[1])
        self.specRepoTable.SetReadOnly(row, 1)
        self.specRepoTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def ClearSelection(self):
        self.specRepoTable.ClearSelection()
        self.deleteSpecRepoBtn.Enable(False)

    def OnAddSpecRepo(self, event):
        self.addSpecDialog = PTAddSpecRepoDialog(self, self.logCallback, self.OnAddSpecRepoCompleteCallback)
        self.addSpecDialog.ShowWindowModal()

    def OnDeleteSpecRepo(self, event):
        row = self.specRepoTable.SelectedRows[0]
        specRepo = self.specRepoData[row]
        PTCommand().removeSpecRepo(specRepo[0], self.logCallback, self.OnDeleteSpecRepoCompleteCallback)

    def OnDeleteSpecRepoCompleteCallback(self, name):
        row = self.specRepoTable.SelectedRows[0]
        specRepo = self.specRepoData[row]

        self.specRepoData.remove(specRepo)
        self.specRepoTable.DeleteRows(row)
        self.ClearSelection()

    def OnCellLeftClick(self, event):
        event.Skip()

        row = event.Row
        self.specRepoTable.ClearSelection()
        self.specRepoTable.SelectRow(row, True)
        self.deleteSpecRepoBtn.Enable(True)

    def OnLabelLeftClick(self, event):
        pass

    def OnAddSpecRepoCompleteCallback(self, name, remotePath):
        self.addSpecDialog.EndModal(0)
        self.addSpecRepo(name, remotePath)

    def addSpecRepo(self, name, remotePath):
        self.ClearSelection()
        self.specRepoData.append((name, remotePath))
        self.AppendSpecRepo(len(self.specRepoData)-1, (name, remotePath))