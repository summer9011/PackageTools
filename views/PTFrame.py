#!/usr/bin/env python
import wx
import wx.aui

from tools.PTCommand import PTCommand

from views.PTEnvironmentWindow import PTEnvironmentWindow
from views.PTCodeRepoWindow import PTCodeRepoWindow
from views.PTSpecRepoWindow import PTSpecRepoWindow
from views.PTModuleWindow import PTModuleWindow
from views.PTLoggerWindow import PTLoggerWindow

from views.PTAddModuleFrame import PTAddModuleFrame
from views.PTAddCodeRepoFrame import PTAddCodeRepoFrame
from views.PTAddSpecRepoFrame import PTAddSpecRepoFrame
from views.PTBranchesFrame import PTBranchesFrame

class PTFrame (wx.Frame):
    mgr = None

    environmentWindow = None
    codeRepoWindow = None
    specRepoWindow = None
    moduleWindow = None
    loggerWindow = None

    addCodeRepoFrame = None
    addSpecRepoFrame = None
    addModuleFrame = None
    branchesFrame = None

    def __init__(self):
        super(PTFrame, self).__init__(None, wx.ID_ANY, u"iOS Develop Tools", size=(800, 600))
        self.SetupUI2()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

    def OnClose(self, event):
        self.mgr.UnInit()
        self.Destroy()

    def SetupUI2(self):
        self.SetBackgroundColour(wx.WHITE)

        self.mgr = wx.aui.AuiManager(self)

        bottomBtnsViewPanel = wx.Panel(self)
        bottomBtnsView = wx.Window(bottomBtnsViewPanel, wx.ID_ANY, size = (0,40))

        btn = wx.Button(bottomBtnsViewPanel, wx.ID_ANY, u"Logger")
        vBox = wx.BoxSizer(wx.HORIZONTAL)
        vBox.Add(btn, 0, wx.LEFT, 10)

        bottomBtnsViewPanelBox = wx.BoxSizer(wx.VERTICAL)
        bottomBtnsViewPanelBox.Add(vBox, 0)
        # bottomBtnsViewPanelBox.Add(bottomBtnsView, 0)
        bottomBtnsViewPanel.SetSizerAndFit(bottomBtnsViewPanelBox)

        # Info
        # infoPanel = wx.Panel(self)
        # infoPanel.SetBackgroundColour(wx.WHITE)
        #
        # topNotebook = wx.Notebook(infoPanel, wx.ID_ANY)
        # self.moduleWindow = PTModuleWindow(topNotebook, self.OnLogCallback, self.OnAddModuleCallback, self.OnBranchesCallback)
        # topNotebook.AddPage(self.moduleWindow, u"Module List")
        # self.specRepoWindow = PTSpecRepoWindow(topNotebook, self.OnLogCallback, self.OnAddSpecRepoCallback)
        # topNotebook.AddPage(self.specRepoWindow, u"Spec Repo List")
        # self.codeRepoWindow = PTCodeRepoWindow(topNotebook, self.OnLogCallback, self.OnAddCodeRepoCallback)
        # topNotebook.AddPage(self.codeRepoWindow, u"Code Repo List")
        # self.environmentWindow = PTEnvironmentWindow(topNotebook, self.OnLogCallback, self.OnEnvironmentImportCallback)
        # topNotebook.AddPage(self.environmentWindow, u"Environment")
        # topNotebook.SetSelection(0)
        #
        # infoBox = wx.BoxSizer(wx.HORIZONTAL)
        # infoBox.Add(topNotebook, 1, wx.EXPAND)
        # infoPanel.SetSizerAndFit(infoBox)
        #
        # centreInfo = wx.aui.AuiPaneInfo().CenterPane()
        # centreInfo.Name("content")
        # centreInfo.CloseButton(False)
        # centreInfo.MaximizeButton(True)
        # self.mgr.AddPane(infoPanel, centreInfo)
        #
        # # Log
        # logPanel = wx.Panel(self)
        # self.loggerWindow = PTLoggerWindow(logPanel)
        #
        # logBox = wx.BoxSizer(wx.HORIZONTAL)
        # logBox.Add(self.loggerWindow, 1, wx.EXPAND)
        # logPanel.SetSizerAndFit(logBox)
        #
        # bottomInfo = wx.aui.AuiPaneInfo().Bottom()
        # bottomInfo.Name("logger")
        # bottomInfo.Caption("Logger")
        # bottomInfo.CloseButton(False)
        # bottomInfo.MinimizeButton(True)
        # self.mgr.AddPane(logPanel, bottomInfo)
        #
        # self.mgr.Update()


    def SetupUI(self):
        panel = wx.Panel(self)

        parentWindow = wx.SplitterWindow(panel, wx.ID_ANY, style=wx.SP_NOBORDER)
        parentWindow.SetBackgroundColour(wx.WHITE)

        # Top window
        topNotebook = wx.Notebook(parentWindow, wx.ID_ANY)
        self.moduleWindow = PTModuleWindow(topNotebook, self.OnLogCallback, self.OnAddModuleCallback, self.OnBranchesCallback)
        topNotebook.AddPage(self.moduleWindow, u"Module List")
        self.specRepoWindow = PTSpecRepoWindow(topNotebook, self.OnLogCallback, self.OnAddSpecRepoCallback)
        topNotebook.AddPage(self.specRepoWindow, u"Spec Repo List")
        self.codeRepoWindow = PTCodeRepoWindow(topNotebook, self.OnLogCallback, self.OnAddCodeRepoCallback)
        topNotebook.AddPage(self.codeRepoWindow, u"Code Repo List")
        self.environmentWindow = PTEnvironmentWindow(topNotebook, self.OnLogCallback, self.OnEnvironmentImportCallback)
        topNotebook.AddPage(self.environmentWindow, u"Environment")
        topNotebook.SetSelection(0)

        # Bottom window
        bottomNotebook = wx.Notebook(parentWindow, wx.ID_ANY)
        self.loggerWindow = PTLoggerWindow(bottomNotebook)
        bottomNotebook.AddPage(self.loggerWindow, u"Logger")

        parentWindow.SplitHorizontally(topNotebook, bottomNotebook, self.GetSize()[1] / 2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(parentWindow, 1, flag=wx.EXPAND)

        panel.SetSizer(sizer)
        panel.Fit()

    # Add code repo callback
    def OnAddCodeRepoCallback(self):
        self.addCodeRepoFrame = PTAddCodeRepoFrame(self, self.OnAddCodeRepoCompleteCallback)

    def OnAddCodeRepoCompleteCallback(self, codeRepo):
        self.addCodeRepoFrame.Destroy()
        self.codeRepoWindow.addCodeRepo(codeRepo)

    # Add spec repo callback
    def OnAddSpecRepoCallback(self):
        self.addSpecRepoFrame = PTAddSpecRepoFrame(self, self.OnAddSpecRepoCompleteCallback)

    def OnAddSpecRepoCompleteCallback(self, specRepo):
        PTCommand().addSpecRepo(specRepo, self.OnLogCallback, self.OnAddSpecRepoToPodCallback)

    def OnAddSpecRepoToPodCallback(self, specRepo):
        self.addSpecRepoFrame.Destroy()
        self.specRepoWindow.addSpecRepo(specRepo)

    # Add module callback
    def OnAddModuleCallback(self):
        self.addModuleFrame = PTAddModuleFrame(self, self.OnAddModuleCompleteCallback, self.codeRepoWindow.codeRepoData, self.specRepoWindow.specRepoData)

    def OnAddModuleCompleteCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        self.moduleWindow.addModule(moduleList[0])

    def OnBranchesCallback(self, module):
        self.branchesFrame = PTBranchesFrame(self, self.OnLogCallback, self.OnBranchesPublishCompleteCallback, module)

    def OnBranchesPublishCompleteCallback(self, result, module):
        self.moduleWindow.OnPublishModuleCompleteCallback(result, module)

    # Environment callback
    def OnEnvironmentImportCallback(self):
        self.moduleWindow.reCreateData()
        self.specRepoWindow.reCreateData()
        self.codeRepoWindow.reCreateData()

    # Log callback
    def OnLogCallback(self, message):
        self.loggerWindow.AppendText(message)