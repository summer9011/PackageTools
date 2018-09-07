#!/usr/bin/env python
import wx

class PTFileDrop(wx.FileDropTarget):
    def __init__(self):
        super(PTFileDrop, self).__init__()

    def OnDropFiles(self, x, y, filenames):
        print filenames
        # wx.LogMessage(filenames[0])