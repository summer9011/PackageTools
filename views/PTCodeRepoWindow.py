#!/usr/bin/env python
import wx
import wx.grid
from tools.PTDBManager import PTDBManager

class PTCodeRepoWindow (wx.Window):
    codeRepoTable = None

    addCodeRepoBtn = None
    deleteCodeRepoBtn = None

    codeRepoData = None

    logCallback = None
    addCodeRepoCallback = None

    def __init__(self, parent, logCallback, addCodeRepoCallback):
        super(PTCodeRepoWindow, self).__init__(parent)

        self.codeRepoData = PTDBManager().getCodeRepoList()
        self.logCallback = logCallback
        self.addCodeRepoCallback = addCodeRepoCallback
        self.SetupUI()

    def SetupUI(self):
        # Table
        self.codeRepoTable = wx.grid.Grid(self, wx.ID_ANY)
        self.codeRepoTable.CreateGrid(0, 4, 1)
        self.codeRepoTable.SetAutoLayout(1)

        self.codeRepoTable.SetColLabelValue(0, u"ID")
        self.codeRepoTable.SetColSize(0, 60)

        self.codeRepoTable.SetColLabelValue(1, u"Type")
        self.codeRepoTable.SetColSize(1, 60)

        self.codeRepoTable.SetColLabelValue(2, u"Name")
        self.codeRepoTable.SetColSize(2, 200)

        self.codeRepoTable.SetColLabelValue(3, u"Remote path")
        self.codeRepoTable.SetColSize(3, 400)

        row = 0
        for codeRepo in self.codeRepoData:
            self.AppendCodeRepo(row, codeRepo)
            row+=1

        self.codeRepoTable.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.codeRepoTable.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

        # Btns
        self.addCodeRepoBtn = wx.Button(self, wx.ID_ANY, u"Add Code Repo")
        self.addCodeRepoBtn.Bind(wx.EVT_BUTTON, self.OnAddCodeRepo)

        self.deleteCodeRepoBtn = wx.Button(self, wx.ID_ANY, u"Delete")
        self.deleteCodeRepoBtn.Bind(wx.EVT_BUTTON, self.OnDeleteCodeRepo)
        self.deleteCodeRepoBtn.Enable(False)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.addCodeRepoBtn, 0, wx.LEFT, 10)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.deleteCodeRepoBtn, 0, wx.RIGHT, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.codeRepoTable, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Fit()

    def AppendCodeRepo(self, row, codeRepo):
        self.codeRepoTable.AppendRows(1)

        self.codeRepoTable.SetRowLabelValue(row, "%d" % (row + 1))
        self.codeRepoTable.SetRowSize(row, 30)

        self.codeRepoTable.SetCellValue(row, 0, "%d" % codeRepo.id)
        self.codeRepoTable.SetReadOnly(row, 0)
        self.codeRepoTable.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.codeRepoTable.SetCellValue(row, 1, codeRepo.typeName())
        self.codeRepoTable.SetReadOnly(row, 1)
        self.codeRepoTable.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.codeRepoTable.SetCellValue(row, 2, codeRepo.name)
        self.codeRepoTable.SetReadOnly(row, 2)
        self.codeRepoTable.SetCellAlignment(row, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        self.codeRepoTable.SetCellValue(row, 3, codeRepo.remotePath)
        self.codeRepoTable.SetReadOnly(row, 3)
        self.codeRepoTable.SetCellAlignment(row, 3, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

    def ClearSelection(self):
        self.codeRepoTable.ClearSelection()
        self.deleteCodeRepoBtn.Enable(False)

    def OnAddCodeRepo(self, event):
        self.addCodeRepoCallback()

    def OnDeleteCodeRepo(self, event):
        row = self.codeRepoTable.SelectedRows[0]
        codeRepo = self.codeRepoData[row]

        PTDBManager().deleteCodeRepo(codeRepo)
        self.codeRepoData.remove(codeRepo)
        self.codeRepoTable.DeleteRows(row)
        self.ClearSelection()

    def OnCellLeftClick(self, event):
        event.Skip()

        row = event.Row
        self.codeRepoTable.ClearSelection()
        self.codeRepoTable.SelectRow(row, True)
        self.deleteCodeRepoBtn.Enable(True)

    def OnLabelLeftClick(self, event):
        pass

    def addCodeRepo(self, codeRepo):
        self.ClearSelection()
        self.codeRepoData.append(codeRepo)
        self.AppendCodeRepo(len(self.codeRepoData)-1, codeRepo)

    def reCreateData(self):
        if len(self.codeRepoData) > 0:
            self.codeRepoTable.DeleteRows(0, len(self.codeRepoData))
            self.codeRepoTable.ClearSelection()

        self.codeRepoData = PTDBManager().getCodeRepoList()
        row = 0
        for codeRepo in self.codeRepoData:
            self.AppendCodeRepo(row, codeRepo)
            row += 1