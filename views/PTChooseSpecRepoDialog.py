#!/usr/bin/env python
import wx
from tools.PTCommand import PTCommandPathConfig
from tools.PTDBManager import PTDBManager

class PTChooseSpecRepoDialog (wx.Dialog):
    chooseSpecTip = None
    specChoice = None

    module = None
    callback = None

    def __init__(self, parent, module, callback):
        super(PTChooseSpecRepoDialog, self).__init__(parent, size=(500, 160))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.module = module
        self.callback = callback

        self.chooseSpecTip = wx.StaticText(self, wx.ID_ANY, u"Select a podspec repo")

        choices = []
        for spec in PTCommandPathConfig.podspecList:
            choices.append(spec[0])
        self.specChoice = wx.Choice(self, wx.ID_ANY, choices=choices)
        if len(choices) > 0:
            self.specChoice.SetSelection(0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((0, 20))
        sizer.Add(self.chooseSpecTip, 0, wx.LEFT, 30)
        sizer.Add((0, 20))
        sizer.Add(self.specChoice, 0, wx.LEFT, 30)
        sizer.Add((0, 20))

        doneBtn = wx.Button(self, wx.ID_ANY, u"Select")
        doneBtn.Bind(wx.EVT_BUTTON, self.OnSelectRepo)

        cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(cancelBtn, 0)
        b.Add((10, 0))
        b.Add(doneBtn, 0)
        sizer.Add(b, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT, 30)

        self.SetSizer(sizer)

    def OnClose(self, event):
        self.EndModal(wx.ID_CANCEL)
        self.callback(True)

    def OnSelectRepo(self, event):
        name, path = PTCommandPathConfig.podspecList[self.specChoice.GetSelection()]
        PTDBManager().updateModuleSpecRepo(self.module, name)
        self.module.sepcName = name
        self.EndModal(wx.ID_OK)
        self.callback(False)

    def OnCancelAction(self, event):
        self.OnClose(event)