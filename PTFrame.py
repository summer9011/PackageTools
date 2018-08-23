#!/usr/bin/env python
import wx
import time
from PTAddModuleFrame import PTAddModuleFrame
from PTAddSpecFrame import PTAddSpecFrame
from PTDBManager import PTDBManager
from PTModule import PTModule
from PTCommand import PTCommand

class PTFrame (wx.Frame):
    addModuleFrame = None
    addSpecFrame = None

    modulePanel = None
    grid = None

    logArea = None

    moduleList = None

    def __init__(self):
        windowSize = wx.DisplaySize()
        size = (800,800)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Develop Kaleidoscope", pos=pos, size=size)
        # self.addStatusBar()
        self.addMenuBar()
        self.addModuleList()

        self.Show(True)

    def addMenuBar(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        addPodSpecItem = fileMenu.Append(wx.ID_ANY, u"Add Pod Spec", u"Add Pod Spec")
        addModuleItem = fileMenu.Append(wx.ID_ANY, u"Add Module", u"Add Module")

        menuBar.Append(fileMenu, u"&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAddPodSpec, addPodSpecItem)
        self.Bind(wx.EVT_MENU, self.OnAddModule, addModuleItem)

    def addStatusBar(self):
        statusBar = wx.StatusBar(self)
        self.SetStatusBar(statusBar)

    def addModuleList(self):
        self.moduleList = PTDBManager().getModuleList()

        self.modulePanel = wx.Panel(self)

        #Tip
        listName = wx.StaticText(self.modulePanel)
        listName.SetLabelText(u"Module List")
        refreshBtn = wx.Button(self.modulePanel, wx.ID_ANY, u"Refresh versions")
        refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshModuleVersions)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(listName, flag=wx.ALIGN_LEFT)
        hbx.Add((10,0))
        hbx.Add(refreshBtn, flag=wx.ALIGN_LEFT)

        self.grid = wx.GridSizer(1, 5, 10, 10)

        #Table header
        rowNameTip = wx.StaticText(self.modulePanel)
        rowNameTip.SetLabelText(u"Module")
        rowRepoSpecTip = wx.StaticText(self.modulePanel)
        rowRepoSpecTip.SetLabelText(u"Repo")
        rowLocalTip = wx.StaticText(self.modulePanel)
        rowLocalTip.SetLabelText(u"Local version")
        rowRemoteTip = wx.StaticText(self.modulePanel)
        rowRemoteTip.SetLabelText(u"Remote version")
        rowOperate = wx.StaticText(self.modulePanel)
        rowOperate.SetLabelText(u"Operate")
        self.grid.AddMany([rowNameTip, rowRepoSpecTip, rowLocalTip, rowRemoteTip, rowOperate])

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
        clearBtn = wx.Button(self.modulePanel, wx.ID_ANY, u"Clear log")
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearLog)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add((10,0))
        hbox3.Add(logTip, flag=wx.ALIGN_LEFT)
        hbox3.Add((10,0))
        hbox3.Add(clearBtn, flag=wx.ALIGN_LEFT)

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
        self.modulePanel.Fit()
        self.refreshVersionsUsingThread()

    def addModule(self, module):
        self.grid.SetRows(self.grid.GetRows()+1)

        nameVal = wx.StaticText(self.modulePanel, module.id*100)
        nameVal.SetLabelText(module.moduleName)
        self.grid.Add(nameVal, 0, wx.EXPAND)

        repoVal = wx.StaticText(self.modulePanel, module.id*100+1)
        repoVal.SetLabelText(module.specId)
        self.grid.Add(repoVal, 0, wx.EXPAND)

        localVal = wx.StaticText(self.modulePanel, module.id*100+2)
        localVal.SetLabelText(module.localVersion)
        self.grid.Add(localVal, 0, wx.EXPAND)

        remoteVal = wx.StaticText(self.modulePanel, module.id*100+3)
        remoteVal.SetLabelText(module.remoteVersion)
        self.grid.Add(remoteVal, 0, wx.EXPAND)

        operateBtn = wx.Button(self.modulePanel, module.id*100+4, u"Publish Module")
        operateBtn.Bind(wx.EVT_BUTTON, self.OnPublishModule)
        operateBtn.Enable(False)
        self.grid.Add(operateBtn, 0, wx.EXPAND)

    def OnPublishModule(self, event):
        moduleId = (event.GetEventObject().GetId()-4)/100

        findModule = None
        for module in self.moduleList:
            if module.id == moduleId:
                findModule = module
                break
        if findModule != None:
            remoteTrunkVersion = PTModule.getModuleTrunkRemoteVersion(findModule, self.OnLogCallback)
            if findModule.localVersion == remoteTrunkVersion:
                self.resetOperationBtn(findModule.id, False, u"Publishing")
                PTCommand().publishModule(findModule, self.OnLogCallback, self.OnPublishModuleCompleteCallback)
            else:
                wx.MessageBox(u"Module (%s) local version is %s, remote trunk version is %s" % (findModule.moduleName, findModule.localVersion, remoteTrunkVersion), u"You should commit all changes using SVN Tools.", wx.OK)

    def OnLogCallback(self, message):
        localTime = time.asctime(time.localtime(time.time()))
        msg = "[%s]%s\n" % (localTime, message)
        self.logArea.AppendText(msg)

    def OnPublishModuleCompleteCallback(self, result, module):
        if result == True:
            PTModule.asyncModuleVersions([module], self.OnLogCallback, self.refreshVersionCallback)

    def refreshVersionsUsingThread(self):
        PTModule.asyncModuleVersions(self.moduleList, self.OnLogCallback, self.refreshVersionCallback)

    def refreshVersionCallback(self, module):
        localVal = self.modulePanel.FindWindowById(module.id*100+2)
        remoteVal = self.modulePanel.FindWindowById(module.id*100+3)
        localVal.SetLabelText(module.localVersion)
        remoteVal.SetLabelText(module.remoteVersion)
        self.resetOperationBtn(module.id, module.isNewer(), u"Publish Module")

    def OnRefreshModuleVersions(self, event):
        self.refreshVersionsUsingThread()

    def OnClearLog(self, event):
        self.logArea.SetValue("")

    def OnAddPodSpec(self, event):
        self.addSpecFrame = PTAddSpecFrame(self.OnAddPodSpecCallback)

    def OnAddPodSpecCallback(self):
        print ""

    def OnAddModule(self, event):
        self.addModuleFrame = PTAddModuleFrame(self.OnAddModuleCallback)

    def OnAddModuleCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        if moduleList != None:
            self.modulePanel.Destroy()
            self.addModuleList()

    def resetOperationBtn(self, moduleId, enable, text):
        operateBtn = self.modulePanel.FindWindowById(moduleId*100+4)
        operateBtn.SetLabelText(text)
        operateBtn.Enable(enable)