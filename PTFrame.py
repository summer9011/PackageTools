#!/usr/bin/env python
import wx
import time
from PTAddModuleFrame import PTAddModuleFrame
from PTAddRepoFrame import PTAddRepoFrame
from PTDBManager import PTDBManager
from PTModule import PTModule
from PTCommand import PTCommand

class PTFrame (wx.Frame):
    addRepoFrame = None
    repoPanel = None
    repoGrid = None
    repoList = None

    addModuleFrame = None
    modulePanel = None
    moduleGrid = None
    moduleList = None

    logPanel = None
    logArea = None

    vbx = None
    repVbox = None
    moduleVbox = None
    logVobx = None

    def __init__(self):
        windowSize = wx.DisplaySize()
        size = (800,1000)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Develop Kaleidoscope", pos=pos, size=size)

        self.addMenuBar()
        self.addRepoList()
        self.addModuleList()
        self.addLogArea()

        self.vbx = wx.BoxSizer(wx.VERTICAL)
        self.vbx.Add(self.repoVbx)
        self.vbx.Add((0, 10))
        self.vbx.Add(self.moduleVbox)
        self.vbx.Add((0, 10))
        self.vbx.Add(self.logVobx)

        self.SetSizer(self.vbx)
        self.Fit()

        self.Show(True)

    def addMenuBar(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        addSpecRepoItem = fileMenu.Append(wx.ID_ANY, u"Add Pod Spec Repo", u"Add Pod Spec Repo")
        addModuleItem = fileMenu.Append(wx.ID_ANY, u"Add Module", u"Add Module")

        menuBar.Append(fileMenu, u"&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAddSpecRepo, addSpecRepoItem)
        self.Bind(wx.EVT_MENU, self.OnAddModule, addModuleItem)

    def addRepoList(self):
        self.repoList = PTDBManager().getRepoList()

        self.repoPanel = wx.Panel(self)
        #Tip
        listName = wx.StaticText(self.repoPanel)
        listName.SetLabelText(u"Repo List")
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(listName, flag=wx.ALIGN_LEFT)

        self.repoVbx = wx.BoxSizer(wx.VERTICAL)
        self.repoVbx.Add((0,30))
        self.repoVbx.Add(hbx, flag=wx.ALIGN_LEFT)

        self.repoPanel.SetSizer(self.repoVbx)
        self.repoPanel.Fit()

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

        self.moduleGrid = wx.GridSizer(1, 5, 10, 10)

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
        self.moduleGrid.AddMany([rowNameTip, rowRepoSpecTip, rowLocalTip, rowRemoteTip, rowOperate])

        #Table rows
        for module in self.moduleList:
            self.addModule(module)

        hbx2 = wx.BoxSizer(wx.HORIZONTAL)
        hbx2.Add((10,0))
        hbx2.Add(self.moduleGrid, flag=wx.ALIGN_CENTER)
        hbx2.Add((10,0))

        self.moduleVbox = wx.BoxSizer(wx.VERTICAL)
        self.moduleVbox.Add((0,30))
        self.moduleVbox.Add(hbx, flag=wx.ALIGN_LEFT)
        self.moduleVbox.Add((0,20))
        self.moduleVbox.Add(hbx2, flag=wx.ALIGN_LEFT)

        self.modulePanel.SetSizer(self.moduleVbox)
        self.modulePanel.Fit()
        self.refreshVersionsUsingThread()

    def addModule(self, module):
        self.moduleGrid.SetRows(self.moduleGrid.GetRows()+1)

        nameVal = wx.StaticText(self.modulePanel, module.id*100)
        nameVal.SetLabelText(module.moduleName)
        self.moduleGrid.Add(nameVal, 0, wx.EXPAND)

        repoVal = wx.StaticText(self.modulePanel, module.id*100+1)
        repoSpec = PTDBManager().getSpecRepo(module.repoId)
        repoText = ""
        if repoSpec.repoName != None:
            repoText = repoSpec.repoName
        repoVal.SetLabelText(repoText)
        self.moduleGrid.Add(repoVal, 0, wx.EXPAND)

        localVal = wx.StaticText(self.modulePanel, module.id*100+2)
        localVal.SetLabelText(module.localVersion)
        self.moduleGrid.Add(localVal, 0, wx.EXPAND)

        remoteVal = wx.StaticText(self.modulePanel, module.id*100+3)
        remoteVal.SetLabelText(module.remoteVersion)
        self.moduleGrid.Add(remoteVal, 0, wx.EXPAND)

        operateBtn = wx.Button(self.modulePanel, module.id*100+4, u"Publish Module")
        operateBtn.Bind(wx.EVT_BUTTON, self.OnPublishModule)
        operateBtn.Enable(False)
        self.moduleGrid.Add(operateBtn, 0, wx.EXPAND)

    def addLogArea(self):
        self.logPanel = wx.Panel(self)

        #Log area
        logTip = wx.StaticText(self.logPanel)
        logTip.SetLabelText(u"Logs: ")
        clearBtn = wx.Button(self.logPanel, wx.ID_ANY, u"Clear log")
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearLog)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add((10,0))
        hbox3.Add(logTip, flag=wx.ALIGN_LEFT)
        hbox3.Add((10,0))
        hbox3.Add(clearBtn, flag=wx.ALIGN_LEFT)

        self.logArea = wx.TextCtrl(self.logPanel, wx.ID_ANY, style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY, size=(770, 400))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add((10,0))
        hbox4.Add(self.logArea, flag=wx.ALIGN_CENTER)
        hbox4.Add((10,0))

        self.logVobx = wx.BoxSizer(wx.VERTICAL)
        self.logVobx.Add((0,30))
        self.logVobx.Add(hbox3, flag=wx.ALIGN_LEFT)
        self.logVobx.Add((0,10))
        self.logVobx.Add(hbox4, flag=wx.ALIGN_LEFT)

        self.logPanel.SetSizer(self.logVobx)
        self.logPanel.Fit()

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

    def OnAddSpecRepo(self, event):
        self.addRepoFrame = PTAddRepoFrame(self.OnAddSpecRepoCallback)

    def OnAddSpecRepoCallback(self, repo):
        PTCommand().addSpecRepo(repo, self.OnLogCallback, self.OnAddSpecRepoToPodCallback)

    def OnAddSpecRepoToPodCallback(self, repo):
        self.addRepoFrame.Destroy()
        if repo != None:
            self.repoPanel.Destroy()
            self.addRepoList()

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