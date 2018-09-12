#!/usr/bin/env python
import wx

class PTFileDrop(wx.FileDropTarget):
    callback = None

    def __init__(self, callback):
        super(PTFileDrop, self).__init__()
        self.callback = callback

    def OnDropFiles(self, x, y, filenames):
        if len(filenames):
            self.callback(filenames[0])
            return True
        return False