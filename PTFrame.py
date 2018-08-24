#!/usr/bin/env python
import wx
import time
from PTAddModuleFrame import PTAddModuleFrame
from PTAddRepoFrame import PTAddRepoFrame
from PTLogFrame import PTLogFrame
from PTDBManager import PTDBManager
from PTModule import PTModule
from PTCommand import PTCommand

class PTFrame (wx.Frame):
    addRepoFrame = None
    addModuleFrame = None
    logFrame = None

    repoList = None
    moduleList = None

    panel = None
    vbx = None

    repoGrid = None
    moduleGrid = None

    def __init__(self):
        windowSize = wx.DisplaySize()
        size = (1000, 600)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Develop Kaleidoscope", pos=(100,100), size=size)

        self.SetMinSize(size)

        self.addMenuBar()
        self.resetViews()
        self.Show(True)

    def resetViews(self):
        self.panel = wx.Panel(self)
        self.vbx = wx.BoxSizer(wx.VERTICAL)

        showLog = wx.Button(self.panel, wx.ID_ANY, u"Logger")
        showLog.Bind(wx.EVT_BUTTON, self.OnDisplayLogger)
        testPod = wx.Button(self.panel, wx.ID_ANY, u"Test Pod Command")
        testPod.Bind(wx.EVT_BUTTON, self.OnTestPodCommand)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(showLog, flag=wx.ALIGN_LEFT)
        hbx.Add((10,0))
        hbx.Add(testPod, flag=wx.ALIGN_LEFT)

        self.vbx.Add((0,10))
        self.vbx.Add(hbx, flag=wx.ALIGN_LEFT)

        self.addRepoList()
        self.addModuleList()

        self.panel.SetSizer(self.vbx)
        self.panel.Fit()

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

        #Tip
        listName = wx.StaticText(self.panel)
        listName.SetLabelText(u"Repo List")
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(listName, flag=wx.ALIGN_LEFT)

        self.repoGrid = wx.GridSizer(1, 4, 10, 10)

        #Table header
        rowNameTip = wx.StaticText(self.panel)
        rowNameTip.SetLabelText(u"Repo name")
        rowRemoteTip = wx.StaticText(self.panel)
        rowRemoteTip.SetLabelText(u"Remote path")
        rowOperate = wx.StaticText(self.panel)
        rowOperate.SetLabelText(u"Operate 1")
        rowDelete = wx.StaticText(self.panel)
        rowDelete.SetLabelText(u"Operate 2")
        self.repoGrid.AddMany([rowNameTip, rowRemoteTip, rowOperate, rowDelete])

        for repo in self.repoList:
            self.addRepo(repo)

        hbx2 = wx.BoxSizer(wx.HORIZONTAL)
        hbx2.Add((10,0))
        hbx2.Add(self.repoGrid, flag=wx.ALIGN_CENTER)
        hbx2.Add((10,0))

        self.vbx.Add((0,30))
        self.vbx.Add(hbx, flag=wx.ALIGN_LEFT)
        self.vbx.Add((0,20))
        self.vbx.Add(hbx2, flag=wx.ALIGN_LEFT)

    def addRepo(self, repo):
        self.repoGrid.SetRows(self.repoGrid.GetRows()+1)

        nameVal = wx.StaticText(self.panel, wx.ID_ANY)
        nameVal.SetLabelText(repo.repoName)
        self.repoGrid.Add(nameVal, 0, wx.EXPAND)

        remoteVal = wx.StaticText(self.panel, wx.ID_ANY)
        remoteVal.SetLabelText(repo.remotePath)
        self.repoGrid.Add(remoteVal, 0, wx.EXPAND)

        operateBtn = wx.Button(self.panel, wx.ID_ANY, u"None")
        operateBtn.Bind(wx.EVT_BUTTON, self.OnRepoOperate)
        operateBtn.Enable(False)
        self.repoGrid.Add(operateBtn, 0, wx.EXPAND)

        deleteBtn = wx.Button(self.panel, repo.id, u"Delete")
        deleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteRepo)
        deleteBtn.Enable(True)
        self.repoGrid.Add(deleteBtn, 0, wx.EXPAND)

    def OnRepoOperate(self, event):
        print "repo operation"

    def OnDeleteRepo(self, event):
        repoId = event.GetEventObject().GetId()

        findRepo = None
        for repo in self.repoList:
            if repo.id == repoId:
                findRepo = repo
                break
        if findRepo != None:
            PTDBManager().deleteSpecRepo(findRepo)
            self.panel.Destroy()
            self.resetViews()

    def addModuleList(self):
        self.moduleList = PTDBManager().getModuleList()

        #Tip
        listName = wx.StaticText(self.panel)
        listName.SetLabelText(u"Module List")
        refreshBtn = wx.Button(self.panel, wx.ID_ANY, u"Refresh versions")
        refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshModuleVersions)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        hbx.Add((10,0))
        hbx.Add(listName, flag=wx.ALIGN_LEFT)
        hbx.Add((10,0))
        hbx.Add(refreshBtn, flag=wx.ALIGN_LEFT)

        self.moduleGrid = wx.GridSizer(1, 6, 10, 10)

        #Table header
        rowNameTip = wx.StaticText(self.panel)
        rowNameTip.SetLabelText(u"Module")
        rowRepoSpecTip = wx.StaticText(self.panel)
        rowRepoSpecTip.SetLabelText(u"Repo")
        rowLocalTip = wx.StaticText(self.panel)
        rowLocalTip.SetLabelText(u"Local version")
        rowRemoteTip = wx.StaticText(self.panel)
        rowRemoteTip.SetLabelText(u"Remote version")
        rowOperate = wx.StaticText(self.panel)
        rowOperate.SetLabelText(u"Operate 1")
        rowDelete = wx.StaticText(self.panel)
        rowDelete.SetLabelText(u"Operate 2")
        self.moduleGrid.AddMany([rowNameTip, rowRepoSpecTip, rowLocalTip, rowRemoteTip, rowOperate, rowDelete])

        #Table rows
        for module in self.moduleList:
            self.addModule(module)

        hbx2 = wx.BoxSizer(wx.HORIZONTAL)
        hbx2.Add((10,0))
        hbx2.Add(self.moduleGrid, flag=wx.ALIGN_CENTER)
        hbx2.Add((10,0))

        self.vbx.Add((0,30))
        self.vbx.Add(hbx, flag=wx.ALIGN_LEFT)
        self.vbx.Add((0,20))
        self.vbx.Add(hbx2, flag=wx.ALIGN_LEFT)

        self.refreshVersionsUsingThread()

    def addModule(self, module):
        self.moduleGrid.SetRows(self.moduleGrid.GetRows()+1)

        nameVal = wx.StaticText(self.panel, module.id*1000)
        nameVal.SetLabelText(module.moduleName)
        self.moduleGrid.Add(nameVal, 0, wx.EXPAND)

        repoVal = wx.StaticText(self.panel, module.id*1000+1)
        repoSpec = PTDBManager().getSpecRepo(module.repoId)
        repoText = ""
        if repoSpec.repoName != None:
            repoText = repoSpec.repoName
        repoVal.SetLabelText(repoText)
        self.moduleGrid.Add(repoVal, 0, wx.EXPAND)

        localVal = wx.StaticText(self.panel, module.id*1000+2)
        localVal.SetLabelText(module.localVersion)
        self.moduleGrid.Add(localVal, 0, wx.EXPAND)

        remoteVal = wx.StaticText(self.panel, module.id*1000+3)
        remoteVal.SetLabelText(module.remoteVersion)
        self.moduleGrid.Add(remoteVal, 0, wx.EXPAND)

        operateBtn = wx.Button(self.panel, module.id*1000+4, u"Publish Module")
        operateBtn.Bind(wx.EVT_BUTTON, self.OnPublishModule)
        operateBtn.Enable(False)
        self.moduleGrid.Add(operateBtn, 0, wx.EXPAND)

        deleteBtn = wx.Button(self.panel, module.id*1000+5, u"Delete")
        deleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteModule)
        deleteBtn.Enable(True)
        self.moduleGrid.Add(deleteBtn, 0, wx.EXPAND)

    def OnDeleteModule(self, event):
        moduleId = (event.GetEventObject().GetId()-4)/1000

        findModule = None
        for module in self.moduleList:
            if module.id == moduleId:
                findModule = module
                break
        if findModule != None:
            PTDBManager().deleteModule(findModule)
            self.panel.Destroy()
            self.resetViews()

    def OnPublishModule(self, event):
        moduleId = (event.GetEventObject().GetId()-4)/1000

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
        self.createLogFrame()
        if self.logFrame.Shown == False:
            self.logFrame.Show(True)
        self.logFrame.appendText(message)

    def OnPublishModuleCompleteCallback(self, result, module):
        if result == True:
            PTModule.asyncModuleVersions([module], self.OnLogCallback, self.refreshVersionCallback)

    def refreshVersionsUsingThread(self):
        PTModule.asyncModuleVersions(self.moduleList, self.OnLogCallback, self.refreshVersionCallback)

    def refreshVersionCallback(self, module):
        localVal = self.panel.FindWindowById(module.id*1000+2)
        remoteVal = self.panel.FindWindowById(module.id*1000+3)
        localVal.SetLabelText(module.localVersion)
        remoteVal.SetLabelText(module.remoteVersion)
        self.resetOperationBtn(module.id, module.isNewer(), u"Publish Module")

    def OnRefreshModuleVersions(self, event):
        self.refreshVersionsUsingThread()

    def OnAddSpecRepo(self, event):
        self.addRepoFrame = PTAddRepoFrame(self.OnAddSpecRepoCallback)

    def OnAddSpecRepoCallback(self, repo):
        PTCommand().addSpecRepo(repo, self.OnLogCallback, self.OnAddSpecRepoToPodCallback)

    def OnAddSpecRepoToPodCallback(self, repo):
        self.addRepoFrame.Destroy()
        if repo != None:
            self.panel.Destroy()
            self.resetViews()

    def OnAddModule(self, event):
        self.addModuleFrame = PTAddModuleFrame(self.OnAddModuleCallback, self.repoList)

    def OnAddModuleCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        if moduleList != None:
            self.panel.Destroy()
            self.resetViews()

    def resetOperationBtn(self, moduleId, enable, text):
        operateBtn = self.panel.FindWindowById(moduleId*1000+4)
        operateBtn.SetLabelText(text)
        operateBtn.Enable(enable)

    def OnDisplayLogger(self, event):
        self.createLogFrame()
        if self.logFrame.Shown == True:
            self.logFrame.Show(False)
        else:
            self.logFrame.Show(True)

    def createLogFrame(self):
        if self.logFrame == None:
            pos = self.GetPosition()
            size = self.GetSize()
            self.logFrame = PTLogFrame((pos[0]+size[0], pos[1]))
            self.logFrame.Bind(wx.EVT_CLOSE, self.OnDestoryLogFrame)

    def OnDestoryLogFrame(self, event):
        self.logFrame.Destroy()
        self.logFrame = None

    def OnTestPodCommand(self, event):
        PTCommand().testPodCommand(self.OnLogCallback)
