#!/usr/bin/env python
import wx

class PTFileDrop(wx.FileDropTarget):
    callback = None
    enterCallback = None

    def __init__(self, callback, enterCallback):
        super(PTFileDrop, self).__init__()
        self.callback = callback
        self.enterCallback = enterCallback

    def OnDropFiles(self, x, y, filenames):
        if len(filenames):
            self.callback(filenames[0])
            return True
        return False

    def OnEnter(self, x, y, defResult):
        self.enterCallback(True)
        return wx.DragMove

    def OnLeave(self):
        self.enterCallback(False)