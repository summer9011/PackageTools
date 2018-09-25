#!/usr/bin/env python
import wx
from views import PTFrame

class PTApp (wx.App):
    def MainLoop(self):
        wx.App.MainLoop(self)


app = PTApp(False)
frame = PTFrame.PTFrame()

# import wx.lib.inspection
# wx.lib.inspection.InspectionTool().Show()

app.MainLoop()
