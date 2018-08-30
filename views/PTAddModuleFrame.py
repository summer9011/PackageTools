#!/usr/bin/env python
import wx
import os
from tools.PTDBManager import PTDBManager
from models.PTModule import  PTModule

class PTAddModuleFrame (wx.Frame):
    localPathTip = None
    localPathText = None
    localPathBtn = None
    codeRepoTip = None
    codeRepoChoice = None
    specRepoTip = None
    specRepoChoice = None

    addBtn = None

    callback = None

    codeRepoList = None
    specRepoList = None

    selectedCodeRepo = None
    selectedSpecRepo = None

    def __init__(self, parent, callback, codeRepoList, specRepoList):
        super(PTAddModuleFrame, self).__init__(parent, wx.ID_ANY, u"Add module", size=(600,220))

        self.codeRepoList = codeRepoList
        self.specRepoList = specRepoList
        self.callback = callback

        gridSizer = wx.FlexGridSizer(3, 2, 10, 10)

        # Local path
        self.localPathTip = wx.StaticText(self)
        self.localPathTip.SetLabelText(u"Trunk path:")
        gridSizer.Add(self.localPathTip, 0)

        self.localPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_READONLY,size=(400, 22))
        self.localPathBtn = wx.Button(self, wx.ID_ANY, u"Choose")
        self.localPathBtn.Bind(wx.EVT_BUTTON, self.OnChooseDirectory)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.localPathText, 1, wx.EXPAND|wx.RIGHT, 10)
        hBox.Add(self.localPathBtn, 0)
        gridSizer.Add(hBox, 1, wx.EXPAND)

        # Code repo
        self.codeRepoTip = wx.StaticText(self)
        self.codeRepoTip.SetLabelText(u"Code repo :")
        gridSizer.Add(self.codeRepoTip, 0)

        codeRepoChoiceList = ['None']
        for codeRepo in codeRepoList:
            codeRepoChoiceList.append(codeRepo.name)
        self.codeRepoChoice = wx.Choice(self, wx.ID_ANY, choices=codeRepoChoiceList, name=u"Code repo list")
        self.codeRepoChoice.Bind(wx.EVT_CHOICE, self.OnChoiceCodeRepo)
        gridSizer.Add(self.codeRepoChoice, 1, wx.EXPAND)

        # Spec repo
        self.specRepoTip = wx.StaticText(self)
        self.specRepoTip.SetLabelText(u"Spec repo :")
        gridSizer.Add(self.specRepoTip, 0)

        specRepoChoiceList = ['None']
        for specRepo in specRepoList:
            specRepoChoiceList.append(specRepo.name)
        self.specRepoChoice = wx.Choice(self, wx.ID_ANY, choices=specRepoChoiceList, name=u"Spec repo list")
        self.specRepoChoice.Bind(wx.EVT_CHOICE, self.OnChoiceSpecRepo)
        gridSizer.Add(self.specRepoChoice, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddModule)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 30)
        sizer.Add(self.addBtn, 0, wx.CENTER|wx.BOTTOM, 30)

        self.SetSizer(sizer)
        self.CentreOnParent()
        self.Show(True)
        self.ShowWithoutActivating()

    def OnChoiceCodeRepo(self, event):
        if event.Selection > 0:
            self.selectedCodeRepo = self.codeRepoList[event.Selection-1]
        else:
            self.selectedCodeRepo = None

    def OnChoiceSpecRepo(self, event):
        if event.Selection > 0:
            self.selectedSpecRepo = self.specRepoList[event.Selection-1]
        else:
            self.selectedSpecRepo = None

    def OnChooseDirectory(self, event):
        dirDlg = wx.DirDialog(self, u"Choose directory", os.path.expanduser('~'), wx.DD_DEFAULT_STYLE)
        if dirDlg.ShowModal() == wx.ID_OK:
            self.localPathText.SetValue(dirDlg.GetPath())

    def OnAddModule(self, event):
        module = PTModule()
        module.localPath = self.localPathText.GetValue()
        module.name = os.path.basename(module.localPath)
        if self.selectedCodeRepo != None:
            module.codeRepoId = self.selectedCodeRepo.id
        else:
            module.codeRepoId = 0

        if self.selectedSpecRepo != None:
            module.specRepoId = self.selectedSpecRepo.id
        else:
            module.specRepoId = 0

        if len(module.localPath) > 0 and module.codeRepoId > 0 and module.specRepoId > 0:
            PTDBManager().addNewModule([module], self.AddModuleCallback)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)

    def AddModuleCallback(self, moduleList):
        self.callback(moduleList)