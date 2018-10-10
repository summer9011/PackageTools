#!/usr/bin/env python
import wx
import wx.aui

from views.PTModuleWindow import PTModuleWindow
from views.PTLoggerWindow import PTLoggerWindow

from views.PTSpecRepoFrame import PTSpecRepoFrame
from views.PTEnvironmentFrame import PTEnvironmentFrame
from views.PTAddLocalModuleFrame import PTAddLocalModuleFrame

class PTFrame (wx.Frame):
    mgr = None

    moduleWindow = None
    loggerWindow = None

    loggerBtn = None

    def __init__(self):
        super(PTFrame, self).__init__(None, wx.ID_ANY, u"iOS Develop Tools", size=(1000, 600))

        self.SetupMenuBar()
        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

        # self.OnDisplayLogger(None)

    def SetupMenuBar(self):
        addMenu = wx.Menu()
        addLocalModuleItem = addMenu.Append(-1, "&Add Local Module...\tCtrl-A", "Add local module")

        fileMenu = wx.Menu()
        specRepoItem = fileMenu.Append(-1, "&Podspec Repo List...\tCtrl-P", "Show Podspec repo list")
        fileMenu.AppendSeparator()
        environmentItem = fileMenu.Append(-1, "&Commands...\tCtrl-E", "Show Commands paths")
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(addMenu, "&Add")
        menuBar.Append(fileMenu, "&Configs")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAddLocalModule,  addLocalModuleItem)
        self.Bind(wx.EVT_MENU, self.OnShowSpecRepoList,  specRepoItem)
        self.Bind(wx.EVT_MENU, self.OnShowCommands,  environmentItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnAddLocalModule(self, event):
        PTAddLocalModuleFrame(self, self.OnLogCallback, self.OnAddLocalModuelCallback)

    def OnAddLocalModuelCallback(self, module, isTrunk):
        self.moduleWindow.OnAddModule(module, isTrunk)

    def OnShowSpecRepoList(self, event):
        PTSpecRepoFrame(self, self.OnLogCallback)

    def OnShowCommands(self, event):
        PTEnvironmentFrame(self, self.OnLogCallback)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        wx.MessageBox("Nice to you.",
                      "Develop Tools",
                      wx.OK|wx.ICON_INFORMATION)

    def OnClose(self, event):
        self.mgr.UnInit()
        self.Destroy()

    def CreateContentWindow(self, panel):
        contentWindow = wx.Window(panel)

        self.mgr = wx.aui.AuiManager(contentWindow)

        panel = wx.Panel(contentWindow)

        topNotebook = wx.Notebook(panel, wx.ID_ANY)
        self.moduleWindow = PTModuleWindow(topNotebook, self.OnLogCallback)
        topNotebook.AddPage(self.moduleWindow, u"Module List")
        topNotebook.SetSelection(0)

        infoBox = wx.BoxSizer(wx.HORIZONTAL)
        infoBox.Add(topNotebook, 1, wx.EXPAND)
        panel.SetSizerAndFit(infoBox)

        centrePane = wx.aui.AuiPaneInfo().CenterPane().Name("content").CloseButton(False)
        self.mgr.AddPane(panel, centrePane)

        panel2 = wx.Panel(contentWindow)
        self.loggerWindow = PTLoggerWindow(panel2)

        logBox = wx.BoxSizer(wx.HORIZONTAL)
        logBox.Add(self.loggerWindow, 1, wx.EXPAND)
        panel2.SetSizerAndFit(logBox)

        leftPane = wx.aui.AuiPaneInfo().Left().Name("logger").CloseButton(False).MinSize((400, 600))
        self.mgr.AddPane(panel2, leftPane)

        self.mgr.Update()

        return contentWindow

    def CreateBottomWindow(self, panel):
        bottomWindow = wx.Window(panel)
        self.loggerBtn = wx.Button(bottomWindow, wx.ID_ANY, u"Hide Logger")
        self.loggerBtn.Bind(wx.EVT_BUTTON, self.OnDisplayLogger)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.loggerBtn, 0)
        bottomWindow.SetSizerAndFit(hBox)

        return bottomWindow

    def OnDisplayLogger(self, event):
        loggerPane = self.mgr.GetPane("logger")
        isShown = loggerPane.IsShown()
        if isShown == True:
            self.loggerBtn.SetLabelText(u"Show Logger")
            loggerPane.Hide()
        else:
            self.loggerBtn.SetLabelText(u"Hide Logger")
            loggerPane.Show(True)
        self.mgr.Update()

    def SetupUI(self):
        self.SetBackgroundColour(wx.WHITE)

        panel = wx.Panel(self)
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.CreateContentWindow(panel), 1, wx.EXPAND)
        vBox.Add(self.CreateBottomWindow(panel), 0, wx.EXPAND)
        panel.SetSizerAndFit(vBox)

    # Log callback
    def OnLogCallback(self, message):
        self.loggerWindow.AppendText(message)