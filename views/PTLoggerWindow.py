#!/usr/bin/env python
import wx
import time

class PTLoggerWindow (wx.Window):
    clearBtn = None
    logArea = None

    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.SetupUI()

    def SetupUI(self):
        self.clearBtn = wx.Button(self, wx.ID_ANY, u"Clear log")
        self.clearBtn.Bind(wx.EVT_BUTTON, self.OnClearLog)
        self.logArea = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.logArea, 1, wx.EXPAND|wx.ALL, 10)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(wx.StaticText(self), 1, wx.EXPAND)
        hBox.Add(self.clearBtn, 0)
        sizer.Add(hBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Fit()

    def OnClearLog(self, event):
        self.logArea.SetValue("")

    def AppendText(self, message):
        localTime = time.asctime(time.localtime(time.time()))
        msg = "[%s]  %s\n" % (localTime, message)
        self.logArea.AppendText(msg)