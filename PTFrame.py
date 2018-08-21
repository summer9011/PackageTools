#!/usr/bin/env python
import wx
from PTAddModuleFrame import PTAddModuleFrame
from PTDBManager import PTDBManager
from PTModule import PTModule

class PTFrame (wx.Frame):
    addModuleFrame = None
    modulePanel = None
    grid = None

    logArea = None

    moduleList = None

    def __init__(self):
        windowSize = wx.DisplaySize()
        size = (800,800)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Develop Kaleidoscope", pos=pos, size=size)
        self.addStatusBar()
        self.addMenuBar()
        self.addModuleList()

        self.Show(True)

    def addMenuBar(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        addItem = fileMenu.Append(wx.ID_ADD, u"Add Module", u"Add Module")

        menuBar.Append(fileMenu, u"&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAddModule, addItem)

    def addStatusBar(self):
        statusBar = wx.StatusBar(self)
        self.SetStatusBar(statusBar)

    def addModuleList(self):
        self.moduleList = PTDBManager().getModuleList()

        self.modulePanel = wx.Panel(self)

        #Tip
        listName = wx.StaticText(self.modulePanel)
        listName.SetLabelText(u"Module List")
        refreshBtn = wx.Button(self.modulePanel, wx.ID_ANY, u"Sync versions")
        refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshModuleVersions)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(listName, flag=wx.ALIGN_LEFT)
        hbx.Add((10,0))
        hbx.Add(refreshBtn, flag=wx.ALIGN_LEFT)

        self.grid = wx.GridSizer(1, 5, 10, 10)

        #Table header
        rowIDTip = wx.StaticText(self.modulePanel)
        rowIDTip.SetLabelText(u"ID")
        rowNameTip = wx.StaticText(self.modulePanel)
        rowNameTip.SetLabelText(u"Module")
        rowLocalTip = wx.StaticText(self.modulePanel)
        rowLocalTip.SetLabelText(u"Local version")
        rowRemoteTip = wx.StaticText(self.modulePanel)
        rowRemoteTip.SetLabelText(u"Remote version")
        rowOperate = wx.StaticText(self.modulePanel)
        rowOperate.SetLabelText(u"Operate")
        self.grid.AddMany([rowIDTip, rowNameTip, rowLocalTip, rowRemoteTip, rowOperate])

        #Table rows
        for module in self.moduleList:
            self.addModule(module)

        hbx2 = wx.BoxSizer(wx.HORIZONTAL)
        hbx2.Add((10,0))
        hbx2.Add(self.grid, flag=wx.ALIGN_CENTER)
        hbx2.Add((10,0))

        #Log area
        logTip = wx.StaticText(self.modulePanel)
        logTip.SetLabelText(u"Logs: ")
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add((10,0))
        hbox3.Add(logTip, flag=wx.ALIGN_LEFT)

        self.logArea = wx.TextCtrl(self.modulePanel, wx.ID_ANY, style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY, size=(770, 400))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add((10,0))
        hbox4.Add(self.logArea, flag=wx.ALIGN_CENTER)
        hbox4.Add((10,0))

        vbx = wx.BoxSizer(wx.VERTICAL)
        vbx.Add((0,30))
        vbx.Add(hbx, flag=wx.ALIGN_LEFT)
        vbx.Add((0,20))
        vbx.Add(hbx2, flag=wx.ALIGN_LEFT)
        vbx.Add((0,30))
        vbx.Add(hbox3, flag=wx.ALIGN_LEFT)
        vbx.Add((0,20))
        vbx.Add(hbox4, flag=wx.ALIGN_LEFT)

        self.modulePanel.SetSizer(vbx)
        self.refreshVersionsUsingThread()

    def addModule(self, module):
        self.grid.SetRows(self.grid.GetRows()+1)

        idVal = wx.StaticText(self.modulePanel)
        idVal.SetLabelText("%d" % (module.id))
        self.grid.Add(idVal, 0, wx.EXPAND)

        nameVal = wx.StaticText(self.modulePanel)
        nameVal.SetLabelText(module.moduleName)
        self.grid.Add(nameVal, 0, wx.EXPAND)

        localVal = wx.StaticText(self.modulePanel)
        localVal.SetLabelText(module.localVersion)
        self.grid.Add(localVal, 0, wx.EXPAND)

        remoteVal = wx.StaticText(self.modulePanel)
        remoteVal.SetLabelText(module.remoteVersion)
        self.grid.Add(remoteVal, 0, wx.EXPAND)

        operateBtn = wx.Button(self.modulePanel, wx.ID_ANY, u"Publish Module")
        operateBtn.Bind(wx.EVT_BUTTON, self.OnPublishModule)
        operateBtn.Enable(False)
        self.grid.Add(operateBtn, 0, wx.EXPAND)

        self.grid.Fit(self.modulePanel)

    def OnPublishModule(self, event):
        print ""

    def refreshVersionsUsingThread(self):
        PTModule.asyncModuleVersions(self.moduleList, self.refreshVersionCallback)

    def refreshVersionCallback(self, module):
        print module

    def OnRefreshModuleVersions(self, event):
        self.refreshVersionsUsingThread()

    def OnAddModule(self, event):
        self.addModuleFrame = PTAddModuleFrame(self.OnAddModuleCallback)

    def OnAddModuleCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        if moduleList != None:
            for module in moduleList:
                self.addModule(module)