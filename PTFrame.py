#!/usr/bin/env python
import wx
import os

class PTFrame (wx.Frame):
    addModuleFrame = None

    localPathTip = None
    localPathText = None
    localPathBtn = None

    def __init__(self):
        windowSize = wx.DisplaySize()
        size = (500, 500)
        pos = ((windowSize[0] - size[0])/2, (windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Develop Kaleidoscope", pos=pos, size=size)
        self.addStatusBar()
        self.addMenuBar()

        self.Show(True)

    def addMenuBar(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        addItem = fileMenu.Append(wx.ID_ADD, u"Add", u"Add Module")

        menuBar.Append(fileMenu, u"&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAddModule, addItem)

    def addStatusBar(self):
        statusBar = wx.StatusBar(self)
        self.SetStatusBar(statusBar)

    def OnAddModule(self, event):
        self.CreateAddModuleFrame()

    def CreateAddModuleFrame(self):
        windowSize = wx.DisplaySize()
        size = (800, 500)
        pos = ((windowSize[0] - size[0])/2, (windowSize[1] - size[1])/2)
        self.addModuleFrame = wx.Frame(None, wx.ID_ANY, u"Add Local module", pos=pos, size=size)

        self.localPathTip = wx.StaticText(self.addModuleFrame)
        self.localPathTip.SetLabelText(u"Local module path:")
        tipBox = wx.BoxSizer(wx.HORIZONTAL)
        tipBox.Add((10, 0))
        tipBox.Add(self.localPathTip, flag=wx.ALIGN_LEFT)

        self.localPathText = wx.TextCtrl(self.addModuleFrame, wx.ID_ANY, style=wx.TE_LEFT|wx.TE_READONLY, size=(500,22))
        self.localPathBtn = wx.Button(self.addModuleFrame, wx.ID_ANY, u"Choose")
        self.localPathBtn.Bind(wx.EVT_BUTTON, self.OnChooseDirectory)
        inputBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.Add((10,0))
        inputBox.Add(self.localPathText, 0, wx.TE_LEFT)
        inputBox.Add((10, 0))
        inputBox.Add(self.localPathBtn, flag=wx.ALIGN_RIGHT)
        inputBox.Add((10,0))

        vboxer = wx.BoxSizer(wx.VERTICAL)
        vboxer.Add((0, 10))
        vboxer.Add(tipBox, flag=wx.ALIGN_LEFT)
        vboxer.Add((0,10))
        vboxer.Add(inputBox, flag=wx.ALIGN_LEFT)

        self.addModuleFrame.SetSizer(vboxer)
        self.addModuleFrame.Show(True)

    def OnChooseDirectory(self, event):
        dirDlg = wx.DirDialog(self.addModuleFrame, u"Choose directory", os.path.expanduser('~'), wx.DD_DEFAULT_STYLE)
        if dirDlg.ShowModal() == wx.ID_OK:
            self.localPathText.SetValue(dirDlg.GetPath())