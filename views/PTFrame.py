#!/usr/bin/env python
import wx
import wx.aui

from tools.PTCommand import PTCommand

from views.PTEnvironmentWindow import PTEnvironmentWindow
from views.PTSpecRepoWindow import PTSpecRepoWindow
from views.PTModuleWindow import PTModuleWindow
from views.PTLoggerWindow import PTLoggerWindow

from views.PTAddSpecRepoFrame import PTAddSpecRepoFrame

class PTFrame (wx.Frame):
    mgr = None

    environmentWindow = None
    specRepoWindow = None
    moduleWindow = None
    loggerWindow = None

    addSpecRepoFrame = None

    loggerBtn = None

    def __init__(self):
        super(PTFrame, self).__init__(None, wx.ID_ANY, u"iOS Develop Tools", size=(800, 600))
        self.SetupUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CentreOnScreen()
        self.Show(True)

        self.OnDisplayLogger(None)

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
        self.specRepoWindow = PTSpecRepoWindow(topNotebook, self.OnLogCallback, self.OnAddSpecRepoCallback)
        topNotebook.AddPage(self.specRepoWindow, u"Spec Repo List")
        self.environmentWindow = PTEnvironmentWindow(topNotebook, self.OnLogCallback)
        topNotebook.AddPage(self.environmentWindow, u"Environment")
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

        bottomPane = wx.aui.AuiPaneInfo().Bottom().Name("logger").CloseButton(False).MinSize((70, 140))
        self.mgr.AddPane(panel2, bottomPane)

        self.mgr.Update()

        return contentWindow

    def CreateBottomWindow(self, panel):
        bottomWindow = wx.Window(panel)
        self.loggerBtn = wx.Button(bottomWindow, wx.ID_ANY, u"Show Logger")
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

    # Add spec repo callback
    def OnAddSpecRepoCallback(self):
        self.addSpecRepoFrame = PTAddSpecRepoFrame(self, self.OnLogCallback, self.OnAddSpecRepoCompleteCallback)

    def OnAddSpecRepoCompleteCallback(self, name, remotePath):
        self.addSpecRepoFrame.Destroy()
        self.specRepoWindow.addSpecRepo(name, remotePath)

    # Log callback
    def OnLogCallback(self, message):
        self.loggerWindow.AppendText(message)