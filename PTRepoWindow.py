#!/usr/bin/env python
import wx
import wx.grid
from PTDBManager import PTDBManager

class PTRepoWindow (wx.Window):
    repoTable = None

    addRepoBtn = None
    deleteRepoBtn = None

    repoData = None

    logCallback = None
    addRepoCallback = None

    def __init__(self, parent, logCallback, addRepoCallback):
        wx.Window.__init__(self, parent)

        self.repoData = PTDBManager().getRepoList()
        self.logCallback = logCallback
        self.addRepoCallback = addRepoCallback
        self.SetupUI()

    def SetupUI(self):
        # Table
        self.repoTable = wx.grid.Grid(self, wx.ID_ANY)
        self.repoTable.CreateGrid(0, 3, 1)
        self.repoTable.SetAutoLayout(1)

        self.repoTable.SetColLabelValue(0, u"ID")
        self.repoTable.SetColSize(0, 60)

        self.repoTable.SetColLabelValue(1, u"Name")
        self.repoTable.SetColSize(1, 200)

        self.repoTable.SetColLabelValue(2, u"Remote path")
        self.repoTable.SetColSize(2, 400)

        row = 0
        for repo in self.repoData:
            self.AppendRepo(row, repo)
            row+=1

        self.repoTable.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.repoTable.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

        # Btns
        self.addRepoBtn = wx.Button(self, wx.ID_ANY, u"Add Spec Repo")
        self.addRepoBtn.Bind(wx.EVT_BUTTON, self.OnAddRepo)

        self.deleteRepoBtn = wx.Button(self, wx.ID_ANY, u"Delete")
        self.deleteRepoBtn.Bind(wx.EVT_BUTTON, self.OnDeleteRepo)
        self.deleteRepoBtn.Enable(False)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.addRepoBtn, 0, wx.LEFT, 10)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.deleteRepoBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.repoTable, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Fit()

    def AppendRepo(self, row, repo):
        self.repoTable.AppendRows(1)

        self.repoTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.repoTable.SetRowSize(row, 30)

        self.repoTable.SetCellValue(row, 0, "%d" % repo.id)
        self.repoTable.SetReadOnly(row, 0)
        self.repoTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.repoTable.SetCellValue(row, 1, repo.repoName)
        self.repoTable.SetReadOnly(row, 1)
        self.repoTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.repoTable.SetCellValue(row, 2, repo.remotePath)
        self.repoTable.SetReadOnly(row, 2)
        self.repoTable.SetCellAlignment(row, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def ClearSelection(self):
        self.repoTable.ClearSelection()
        self.deleteRepoBtn.Enable(False)

    def OnAddRepo(self, event):
        self.addRepoCallback()

    def OnDeleteRepo(self, event):
        row = self.repoTable.SelectedRows[0]
        repo = self.repoData[row]

        PTDBManager().deleteSpecRepo(repo)
        self.repoData.remove(repo)
        self.repoTable.DeleteRows(row)
        self.ClearSelection()

    def OnCellLeftClick(self, event):
        event.Skip()

        row = event.Row
        self.repoTable.ClearSelection()
        self.repoTable.SelectRow(row, True)
        self.deleteRepoBtn.Enable(True)

    def OnLabelLeftClick(self, event):
        pass

    def addRepo(self, repo):
        self.ClearSelection()
        self.repoData.append(repo)
        self.AppendRepo(len(self.repoData)-1, repo)