#!/usr/bin/env python
import wx

from PTAddModuleFrame import PTAddModuleFrame
from PTAddSpecRepoFrame import PTAddSpecRepoFrame
from PTCommand import PTCommand

from PTEnvironmentWindow import PTEnvironmentWindow
from PTSpecRepoWindow import PTSpecRepoWindow
from PTModuleWindow import PTModuleWindow
from PTLoggerWindow import PTLoggerWindow

class PTFrame (wx.Frame):
    environmentWindow = None
    specRepoWindow = None
    moduleWindow = None
    loggerWindow = None

    addSpecRepoFrame = None
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
        self.specRepoWindow = PTSpecRepoWindow(topNotebook, self.OnLogCallback, self.OnAddSpecRepoCallback)
        topNotebook.AddPage(self.specRepoWindow, u"Spec Repo List")
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
        self.addModuleFrame = PTAddModuleFrame(self, self.OnAddModuleCompleteCallback, self.specRepoWindow.specRepoData)

    def OnAddModuleCompleteCallback(self, moduleList):
        self.addModuleFrame.Destroy()
        self.moduleWindow.addModule(moduleList[0])
