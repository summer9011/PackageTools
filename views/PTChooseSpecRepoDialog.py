#!/usr/bin/env python
import wx

class PTChooseSpecRepoDialog (wx.Dialog):
    progressTip = None
    progress = None

    module = None
    callback = None

    def __init__(self, parent, module, callback):
        super(PTChooseSpecRepoDialog, self).__init__(parent, size=(500,160))