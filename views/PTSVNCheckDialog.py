#!/usr/bin/env python
import wx
from tools.PTCommand import PTCommand

class PTSVNCheckDialog (wx.Dialog):
    tipText1 = None
    tipText2 = None

    okBtn = None
    cancelBtn = None

    path = None
    logCallback = None
    callback = None

    notWorkingCopy = True

    def __init__(self, parent, path, notWorkingCopy, message, logCallback, callback):
        if notWorkingCopy == True:
            tip2 = u"Please choose your module working copy."
            okBtnText = u"Done"
            height = 180
        else:
            tip2 = u"You should restart your SVN Client app when Click \"SVN Upgrade\", if using \"Cornerstone\" or other apps."
            okBtnText = u"SVN Upgrade"
            height = 260

        super(PTSVNCheckDialog, self).__init__(parent, size=(500, height))

        self.path = path
        self.notWorkingCopy = notWorkingCopy
        self.logCallback = logCallback
        self.callback = callback

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.tipText1 = wx.StaticText(self, wx.ID_ANY, message)
        self.tipText1.Wrap(460)
        sizer.Add((0, 20))
        sizer.Add(self.tipText1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)


        self.tipText2 = wx.StaticText(self, wx.ID_ANY, tip2)
        self.tipText2.Wrap(460)
        sizer.Add((0, 20))
        sizer.Add(self.tipText2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)

        self.okBtn = wx.Button(self, wx.ID_ANY, okBtnText)
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOKAction)

        self.cancelBtn = wx.Button(self, wx.ID_ANY, u"Cancel")
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelAction)

        b = wx.BoxSizer(wx.HORIZONTAL)
        b.Add(self.cancelBtn)
        b.Add((10,0))
        b.Add(self.okBtn)
        sizer.Add((0, 20))
        sizer.Add(b, 0, wx.ALIGN_RIGHT|wx.RIGHT, 20)
        sizer.Add((0, 20))

        self.SetSizer(sizer)

    def OnOKAction(self, event):
        if self.notWorkingCopy == True:
            self.OnCancelAction(event)
        else:
            PTCommand().svnUpgrade(self.path, self.logCallback, self.OnSVNUpgradeCallback)

    def OnSVNUpgradeCallback(self, success, result):
        self.callback(success, self.path)
        if success != 0:
            wx.MessageBox(u"Svn upgrade failed. \n%s" % result, u"Error", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def OnCancelAction(self, event):
        self.EndModal(wx.ID_OK)