#!/usr/bin/env python
import wx
import PTApp
import PTFrame

app = PTApp.PTApp(False)
frame = PTFrame.PTFrame()
app.MainLoop()