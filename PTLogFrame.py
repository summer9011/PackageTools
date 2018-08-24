#!/usr/bin/env python
import wx
import time

class PTLogFrame (wx.Frame):
    logArea = None

    panel = None

    def __init__(self, pos):
        size = (600,400)
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Logger", pos=pos, size=size)

        self.addLogArea()

    def addLogArea(self):
        panel = wx.Panel(self)

        #Log area
        logTip = wx.StaticText(panel)
        logTip.SetLabelText(u"Logs: ")
        clearBtn = wx.Button(panel, wx.ID_ANY, u"Clear log")
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearLog)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add((10,0))
        hbox3.Add(logTip, flag=wx.ALIGN_LEFT)
        hbox3.Add((10,0))
        hbox3.Add(clearBtn, flag=wx.ALIGN_LEFT)

        self.logArea = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY, size=(580, 300))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add((10,0))
        hbox4.Add(self.logArea, flag=wx.ALIGN_CENTER)
        hbox4.Add((10,0))

        vbx = wx.BoxSizer(wx.VERTICAL)
        vbx.Add((0,30))
        vbx.Add(hbox3)
        vbx.Add((0,10))
        vbx.Add(hbox4)
        panel.SetSizer(vbx)
        panel.Fit()

    def appendText(self, msg):
        localTime = time.asctime(time.localtime(time.time()))
        msg = "[%s]%s\n" % (localTime, msg)
        self.logArea.AppendText(msg)

    def OnClearLog(self, event):
        self.logArea.SetValue("")
