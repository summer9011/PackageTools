#!/usr/bin/env python
import wx

from PTAddModuleFrame import PTAddModuleFrame
from PTAddRepoFrame import PTAddRepoFrame
from PTCommand import PTCommand

from PTEnvironmentWindow import PTEnvironmentWindow
from PTRepoWindow import PTRepoWindow
from PTModuleWindow import PTModuleWindow
from PTLoggerWindow import PTLoggerWindow

class PTFrame (wx.Frame):
    environmentWindow = None
    repoWindow = None
    moduleWindow = None
    loggerWindow = None

    addRepoFrame = None
    addModuleFrame = None

    def __init__(self):
        displaySize = wx.GetDisplaySize()
        size = (800, 800)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"iOS Develop Tools", pos=((displaySize[0]-size[0])/2, (displaySize[1]-size[1])/2), size=size)
        self.SetMinSize(size)
        self.SetupUI()
        self.Show(True)

    def SetupUI(self):
        panel = wx.Panel(self)

        parentWindow = wx.SplitterWindow(panel, wx.ID_ANY, style=wx.SP_NOBORDER)
        parentWindow.SetBackgroundColour(wx.WHITE)

        # Top window
        topNotebook = wx.Notebook(parentWindow, wx.ID_ANY)
        self.environmentWindow = PTEnvironmentWindow(topNotebook, self.OnLogCallback)
        topNotebook.AddPage(self.environmentWindow, u"Environment")
        self.repoWindow = PTRepoWindow(topNotebook, self.OnLogCallback, self.OnAddSpecRepoCallback)
        topNotebook.AddPage(self.repoWindow, u"Spec Repo List")
        self.moduleWindow = PTModuleWindow(topNotebook, self.OnLogCallback, self.OnAddModuleCallback)
        topNotebook.AddPage(self.moduleWindow, u"Module List")

        topNotebook.SetSelection(2)

        # Bottom window
        bottomNotebook = wx.Notebook(parentWindow, wx.ID_ANY)
        self.loggerWindow = PTLoggerWindow(bottomNotebook)
        bottomNotebook.AddPage(self.loggerWindow, u"Logger")

        parentWindow.SplitHorizontally(topNotebook, bottomNotebook, self.GetSize()[1] / 2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(parentWindow, 1, flag=wx.EXPAND)

        panel.SetSizer(sizer)
        panel.Fit()

    # Log callback
    def OnLogCallback(self, message):
        self.loggerWindow.AppendText(message)

    # Add repo callback
    def OnAddSpecRepoCallback(self):
        self.addRepoFrame = PTAddRepoFrame(self, self.OnAddSpecRepoCompleteCallback)

    def OnAddSpecRepoCompleteCallback(self, repo):
        PTCommand().addSpecRepo(repo, self.OnLogCallback, self.OnAddSpecRepoToPodCallback)

    def OnAddSpecRepoToPodCallback(self, repo):
        self.addRepoFrame.Destroy()
        self.repoWindow.addRepo(repo)

    # Add module callback
    def OnAddModuleCallback(self):
        self.addModuleFrame = PTAddModuleFrame(self, self.OnAddModuleCompleteCallback, self.repoWindow.repoData)

    def OnAddModuleCompleteCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        self.moduleWindow.addModule(moduleList[0])
