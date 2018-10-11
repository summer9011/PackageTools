#!/usr/bin/env python
import wx
import wx.dataview

class PTSVNCommitFrame (wx.Frame):
    dataListView = None
    selectAllBtn = None

    commitMsgText = None
    commitBtn = None
    cancelBtn = None

    files = None
    logCallback = None
    callback = None

    def __init__(self, parent, files, logCalllback, callback):
        super(PTSVNCommitFrame, self).__init__(parent, wx.ID_ANY, u"Choose files to commit", size=(600, 400), style= wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU)

        self.files = files
        self.logCallback = logCalllback
        self.callback = callback

        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.Destroy()
        self.callback(True)

    def SetupUI(self):
        self.dataListView = wx.dataview.DataViewListCtrl(self, style=wx.dataview.DV_MULTIPLE)
        self.dataListView.AppendTextColumn(u"Status", 0, width=40)
        self.dataListView.AppendTextColumn(u"Name", 1, width=400)
        self.dataListView.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.DataViewSelectedRow)

        for (status, name) in self.files:
            self.dataListView.AppendItem([status, name])

        self.selectAllBtn = wx.Button(self, wx.ID_ANY, u"Select All")
        self.selectAllBtn.Bind(wx.EVT_BUTTON, self.OnSelectAll)

        commitMsg = wx.StaticText(self, wx.ID_ANY, u"Commit Messages:")

        self.commitMsgText = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(600, 60))
        self.commitMsgText.Bind(wx.EVT_TEXT, self.OnCommitMsgChange)

        self.commitBtn = wx.Button(self, wx.ID_ANY, u"Commit")
        self.commitBtn.Bind(wx.EVT_BUTTON, self.OnCommitFiles)
        self.commitBtn.Enable(False)

        self.cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelCommit)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(self.cancelBtn, 0, wx.RIGHT, 30)
        b.Add(self.commitBtn, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dataListView, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.selectAllBtn, 0, wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        sizer.Add(commitMsg, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 10)
        sizer.Add(self.commitMsgText, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(b, 0, wx.ALIGN_RIGHT|wx.ALL, 10)

        self.SetSizer(sizer)

        self.dataListView.SetFocus()

    def DataViewSelectedRow(self, event):
        if len(self.commitMsgText.GetValue()) > 0 and self.dataListView.SelectedItemsCount > 0:
            self.commitBtn.Enable(True)
            return
        self.commitBtn.Enable(False)

    def OnSelectAll(self, event):
        if self.dataListView.SelectedItemsCount == len(self.files):
            self.dataListView.UnselectAll()
            self.selectAllBtn.SetLabel("Select All")
        else:
            self.dataListView.SelectAll()
            self.selectAllBtn.SetLabel("Unselect All")

    def OnCommitMsgChange(self, event):
        if len(self.commitMsgText.GetValue()) > 0 and self.dataListView.SelectedItemsCount > 0:
            self.commitBtn.Enable(True)
            return
        self.commitBtn.Enable(False)

    def OnCommitFiles(self, event):
        commitList = []
        addList = []
        deleteList = []
        for item in self.dataListView.Selections:
            if item != None:
                row = self.dataListView.ItemToRow(item)
                file = self.files[row]
                if file[0] == "?":
                    addList.append(file[1])
                elif file[0] == "!":
                    deleteList.append(file[1])
                else:
                    commitList.append(file[1])
        self.Destroy()
        self.callback(False, commitList, addList, deleteList, self.commitMsgText.GetValue())

    def OnCancelCommit(self, event):
        self.OnClose(event)