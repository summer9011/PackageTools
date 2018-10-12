#!/usr/bin/env python
import wx

class PTDeleteDialog (wx.Dialog):
    module = None
    callback = None

    def __init__(self, parent, module, callback):
        super(PTDeleteDialog, self).__init__(parent, size=(500,140))

        self.module = module
        self.callback = callback

        sizer = wx.BoxSizer(wx.VERTICAL)

        tip = wx.StaticText(self, wx.ID_ANY, u"Click \"Yes\" to delete module (%s)" % module.name)
        sizer.Add((0, 20))
        sizer.Add(tip, 0, wx.CENTER|wx.RIGHT|wx.LEFT, 30)
        sizer.Add((0, 40))

        yesBtn = wx.Button(self, wx.ID_ANY, u"Yes")
        yesBtn.Bind(wx.EVT_BUTTON, self.OnDeleteAction)

        noBtn = wx.Button(self, wx.ID_ANY, u"No")
        noBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(wx.StaticText(self), 1)
        b.Add(noBtn)
        b.Add((10, 0))
        b.Add(yesBtn)
        sizer.Add(b, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 30)

        self.SetSizer(sizer)

    def OnDeleteAction(self, event):
        self.callback(True)
        self.EndModal(wx.ID_OK)

    def OnCancelAction(self, event):
        self.callback(False)
        self.EndModal(wx.ID_OK)